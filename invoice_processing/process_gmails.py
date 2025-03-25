"""Processes Gmail messages to identify and extract invoice details."""

import base64
import json
import time
import traceback

from autokitteh.google import gmail_client

import openAI_handling
import scan_gmails
import schemas


gmail = gmail_client("gmail_conn").users()


def is_message_invoice(message_body, message_attachments, message_images):
    """Determine if a message contains an invoice."""
    print("Checking if message is an invoice...")

    # Use specific instructions that clearly request a simple True/False response.
    instructions = """
    You are a helper that determines if attached files are an invoice or receipt.
    IMPORTANT: Analyze all files and respond with ONLY 'True' or 'False'.
    - If ANY file is an invoice or receipt, respond with 'True'
    - Otherwise, respond with 'False'
    Do not include any explanations, just True or False.
    """

    # Get the raw text response from AI.
    is_invoice_response = openAI_handling.send_ai_request(
        message_body,
        message_attachments,
        message_images,
        instructions,
        schemas.AI_BOOLEAN_SCHEMA,
    )

    # Handle response as text.
    if not is_invoice_response:
        print("No response received from AI")
        return False

    # Parse text response - accept variations of true/yes.
    cleaned_response = is_invoice_response.strip().lower()

    # Check for positive responses.
    true_indicators = ["true", "yes", "1", "correct", "invoice", "receipt"]

    # Return True if any indicator is found in the response.
    for indicator in true_indicators:
        if indicator in cleaned_response:
            print(f"Found '{indicator}' in response - considering this an invoice")
            return True

    return False


def try_parse_json(response):
    """Attempt to parse JSON response with required invoice fields."""
    try:
        parsed_json = json.loads(response)
    except json.JSONDecodeError:
        parsed_json = {}

    required_keys = ["companyName", "date", "amount", "invoiceId"]
    if not all(key in parsed_json for key in required_keys):
        parsed_json = {}

    return parsed_json


def parse_invoice_to_json(message_body, message_attachments, message_images):
    """Extract invoice details into structured JSON."""
    max_retries = 3

    instructions = """
    Please extract information from the uploaded invoice files (PDF or images).
    For each invoice, extract:
    1. Company name (who issued the invoice)
    2. Invoice date
    3. Total amount (with currency)
    4. Invoice ID or number
    Return ONLY a JSON object with these fields:
    {
      "companyName": "Example Corp",
      "date": "2023-01-15",
      "amount": "$123.45",
      "invoiceId": "INV-12345"
    }
    """

    for attempt in range(max_retries):
        json_invoice = openAI_handling.send_ai_request(
            message_body,
            message_attachments,
            message_images,
            instructions,
            schemas.AI_INVOICE_JSON_SCHEMA,
        )

        if json_invoice:
            parsed_json = try_parse_json(json_invoice)
            if parsed_json:
                return parsed_json

        if attempt < max_retries - 1:
            print(f"Retrying invoice parsing... ({attempt + 1}/{max_retries})")
            time.sleep(2)  # Brief pause before retry.

    return None


def handle_scan(ts):
    """Scan emails since timestamp ts and process for invoices."""
    invoices = []

    try:
        messages = scan_gmails.scan_gmail_messages(ts)

        for idx, msg in enumerate(messages):
            print(f"Processing message {idx + 1}/{len(messages)}")

            # Rate limiting.
            time.sleep(5)

            # Check if message is an invoice.
            is_email_invoice = is_message_invoice(
                msg["body"], msg["attachments"], msg["images"]
            )

            if is_email_invoice:
                # Parse invoice details.
                message_json_parsed = parse_invoice_to_json(
                    msg["body"], msg["attachments"], msg["images"]
                )

                if message_json_parsed:
                    invoices.append(message_json_parsed)
            else:
                print(f"Message {msg['id']} is not an invoice")

    except json.JSONDecodeError as e:
        print(f"Error in handle_scan: {e}")
        traceback.print_exc()

    return invoices


def send_invoices(invoices):
    """Send an email report with processed invoices."""
    try:
        profile = gmail.getProfile(userId="me").execute()

        if not invoices:
            mail_body = "No invoices found for this period."
        else:
            mail_body = json.dumps(invoices, indent=4)

        msg = f"""From: {profile["emailAddress"]}
To: {profile["emailAddress"]}
Subject: Invoice Processing Report

{mail_body}"""

        # Format message for Gmail API
        msg = msg.replace("\n", "\r\n")
        msg = base64.urlsafe_b64encode(msg.encode()).decode()

        gmail.messages().send(userId="me", body={"raw": msg}).execute()
        print("Invoice report sent successfully!")

    except json.JSONDecodeError as e:
        print(f"Unexpected error sending invoice report: {str(e)}")

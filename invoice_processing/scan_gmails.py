"""Scan Gmail messages and extract content.

Including subject, body, PDF attachments, and image attachments.
"""

import base64
from datetime import datetime, UTC

from autokitteh.google import gmail_client


IMAGE_MIME_TYPES = [
    "image/bmp",  # Not sure if works, need to check.
    "image/gif",  # Not sure if works, need to check.
    "image/jpeg",  # Not sure if works, need to check.
    "image/png",
    "image/tiff",  # Not sure if works, need to check.
    "image/webp",  # Not sure if works, need to check.
]

TEXT_MIME_TYPES = [
    "text/html",
    "text/plain",
]

gmail = gmail_client("gmail_conn").users()


def is_image(part):
    recognized_type = part.get("mimeType") in IMAGE_MIME_TYPES
    return recognized_type and "attachmentId" not in part.get("body", {})


def is_pdf(part):
    recognized_type = part.get("mimeType") == "application/pdf"
    return recognized_type and "attachmentId" in part.get("body", {})


def is_text(part):
    recognized_type = part.get("mimeType") in TEXT_MIME_TYPES
    return recognized_type and "data" in part.get("body", {})


def get_mail_content(message):
    subject = get_subject(message)
    body = get_body(message)
    pdf_files = get_pdf_attachments(message)
    images = get_image_attachments(message)
    return subject, body, pdf_files, images


def get_subject(message):
    """Extract subject from message headers."""
    headers = message.get("payload", {}).get("headers", [])
    return next(
        (header["value"] for header in headers if header["name"].lower() == "subject"),
        "No Subject",
    )


def get_body(message):
    payload = message.get("payload", {})

    for part in payload.get("parts", []):
        if part["mimeType"] == "multipart/alternative":
            for sub_part in part.get("parts", []):
                if is_text(sub_part):
                    return process_body_part(sub_part)
        elif is_text(part):
            return process_body_part(part)

    return "No body content"


def process_body_part(part):
    data = part["body"]["data"]
    return base64.urlsafe_b64decode(data).decode("utf-8")


def get_pdf_attachments(message):
    """Extract PDF attachments from message."""
    pdf_files = []

    payload = message.get("payload", {})
    for part in [part for part in payload.get("parts", []) if is_pdf(part)]:
        client = gmail.messages().attachments()
        attachment = client.get(
            userId="me", messageId=message["id"], id=part["body"]["attachmentId"]
        ).execute()

        if "data" not in attachment:
            continue

        pdf_files.append(
            {
                "filename": part.get("filename", "unnamed.pdf"),
                "data": base64url_to_base64(attachment),
            }
        )

    return pdf_files


def base64url_to_base64(attachment):
    data = base64.urlsafe_b64decode(attachment["data"])
    return base64.b64encode(data).decode("utf-8")


def get_image_attachments(message):
    """Extract images from message, including from nested multipart messages."""
    image_files = []
    payload = message.get("payload", {})

    def process_part(part):
        if part.get("mimeType") == "multipart/alternative":
            for sub_part in part.get("parts", []):
                process_part(sub_part)

        elif is_image(part):
            try:
                client = gmail.messages().attachments()
                attachment = client.get(
                    userId="me",
                    messageId=message["id"],
                    id=part["body"]["attachmentId"],
                ).execute()

                if attachment.get("data"):
                    mime_type = part.get("mimeType", "image/png")
                    encoded_data = base64url_to_base64(attachment)

                    # Create proper image URL format.
                    data_url = f"data:{mime_type};base64,{encoded_data}"

                    image_files.append({"data": data_url})

            except (KeyError, TypeError) as e:
                print(f"Error processing image attachment: {str(e)}")
                return  # Use return instead of continue.

    # Process all parts.
    if "parts" in payload:
        for part in payload["parts"]:
            process_part(part)
    elif is_image(payload):
        process_part(payload)

    return image_files


def scan_gmail_messages(ts):
    """Scans Gmail for messages based on a timestamp (ts)."""
    date_from = datetime.fromtimestamp(ts, tz=UTC).strftime("%Y/%m/%d")
    messages = gmail.messages().list(userId="me", q=f"after:{date_from}").execute()
    emails = []

    for msg in messages.get("messages", []):
        message = gmail.messages().get(userId="me", id=msg["id"]).execute()
        subject, body, pdf_files, images = get_mail_content(message)

        attachments = []
        for pdf in pdf_files:
            attachment = {"filename": pdf["filename"], "data": pdf["data"]}
            attachments.append(attachment)

        mail_data = {
            "id": message["id"],
            "subject": subject,
            "body": body,
            "images": images or [],
            "attachments": attachments,
        }
        emails.append(mail_data)

    return emails

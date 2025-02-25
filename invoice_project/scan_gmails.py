import base64
from datetime import datetime, UTC

from autokitteh.google import gmail_client


gmail = gmail_client("gmail_conn").users()


def get_mail_content(message):
    subject = get_subject(message)
    body = get_body(message)
    pdf_files = get_pdf_attachments(message)
    images = get_image_attachments(message)
    return subject, body, pdf_files, images


def get_subject(message):
    """Extract subject from message headers"""
    headers = message.get("payload", {}).get("headers", [])
    return next(
        (header["value"] for header in headers if header["name"].lower() == "subject"),
        "No Subject",
    )


def get_body(message):
    payload = message.get("payload", {})
    parts = payload.get("parts", [])

    for part in parts:
        if part["mimeType"] == "multipart/alternative":
            for sub_part in part.get("parts", []):
                if sub_part["mimeType"] == "text/plain" and "data" in sub_part.get(
                    "body", {}
                ):
                    body_data = sub_part["body"]["data"]
                    return base64.urlsafe_b64decode(body_data).decode("utf-8")
                elif sub_part["mimeType"] == "text/html" and "data" in sub_part.get(
                    "body", {}
                ):
                    body_data = sub_part["body"]["data"]
                    return base64.urlsafe_b64decode(body_data).decode("utf-8")
        elif part["mimeType"] == "text/plain" and "data" in part.get("body", {}):
            body_data = part["body"]["data"]
            return base64.urlsafe_b64decode(body_data).decode("utf-8")
        elif part["mimeType"] == "text/html" and "data" in part.get("body", {}):
            body_data = part["body"]["data"]
            return base64.urlsafe_b64decode(body_data).decode("utf-8")

    return "No body content"


def get_pdf_attachments(message):
    """Extract PDF attachments from message"""
    pdf_files = []
    payload = message.get("payload", {})

    if "parts" not in payload:
        return pdf_files

    for part in payload["parts"]:
        if part["mimeType"] != "application/pdf" or "attachmentId" not in part.get(
            "body", {}
        ):
            continue

        attachment = (
            gmail.messages()
            .attachments()
            .get(userId="me", messageId=message["id"], id=part["body"]["attachmentId"])
            .execute()
        )

        if attachment.get("data"):
            pdf_files.append(
                {
                    "filename": part.get("filename", "unnamed.pdf"),
                    "data": base64.b64encode(
                        base64.urlsafe_b64decode(attachment["data"])
                    ).decode("utf-8"),
                }
            )

    return pdf_files


def get_image_attachments(message):
    """Extract images from message, including from nested multipart messages"""
    image_files = []
    payload = message.get("payload", {})

    image_mime_types = [
        "image/jpeg",  # not sure if works, need to check
        "image/png",
        "image/gif",  # not sure if works, need to check
        "image/bmp",  # not sure if works, need to check
        "image/tiff",  # not sure if works, need to check
        "image/webp",  # not sure if works, need to check
    ]

    def process_part(part):
        if part.get("mimeType") == "multipart/alternative":
            for sub_part in part.get("parts", []):
                process_part(sub_part)
        elif part.get("mimeType") in image_mime_types and "attachmentId" in part.get(
            "body", {}
        ):
            try:
                attachment = (
                    gmail.messages()
                    .attachments()
                    .get(
                        userId="me",
                        messageId=message["id"],
                        id=part["body"]["attachmentId"],
                    )
                    .execute()
                )

                if attachment.get("data"):
                    mime_type = part.get("mimeType", "image/png")
                    # Convert from base64url to standard base64
                    image_data = base64.urlsafe_b64decode(attachment["data"])
                    encoded_data = base64.b64encode(image_data).decode("utf-8")

                    # Create proper image URL format
                    data_url = f"data:{mime_type};base64,{encoded_data}"

                    image_files.append({"data": data_url})

            except Exception as e:
                print(f"Error processing image attachment: {str(e)}")
                return  # Use return instead of continue

    # Process all parts
    if "parts" in payload:
        for part in payload["parts"]:
            process_part(part)
    elif payload.get("mimeType") in image_mime_types and "attachmentId" in payload.get(
        "body", {}
    ):
        process_part(payload)

    return image_files


def scan_gmail_messages(ts):
    """Scans Gmail for messages based on a timestamp (ts)"""
    date_from = datetime.fromtimestamp(ts, tz=UTC).strftime("%Y/%m/%d")
    messages = gmail.messages().list(userId="me", q=f"after:{date_from}").execute()
    emails = []
    for msg in messages.get("messages", []):
        message = gmail.messages().get(userId="me", id=msg["id"]).execute()
        subject, body, pdf_files, images = get_mail_content(message)
        mail_data = {
            "id": message["id"],
            "subject": subject,
            "body": body,
            "images": images if images else [],
            "attachments": [
                {"filename": pdf["filename"], "data": pdf["data"]} for pdf in pdf_files
            ]
            if pdf_files
            else [],
        }
        emails.append(mail_data)
    return emails

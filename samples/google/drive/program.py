"""Autokitteh's Google Drive integration to monitor changes to files."""

import os

from autokitteh.google import google_drive_client


USER_EMAIL = os.getenv("USER_EMAIL", "")


def on_file_change(event):
    print(f"File with ID {event.data.file_id} has changed!")


def on_file_remove(event):
    print(f"File with ID {event.data.file_id} has been removed!")


def create_new_document(_):
    """Creates a new Google Document and optionally shares it with a specified user.

    If the Google Drive permission scope is limited to https://www.googleapis.com/auth/drive.file,
    the app must create a new file to enable change monitoring. Note that creating a
    file is not the only way to grant permissions; there are other options detailed
    here: https://developers.google.com/drive/api/guides/manage-sharing. For example,
    when using a service account, you can share a specific file with the service
    account's email address.
    """
    client = google_drive_client("google_drive_conn")

    file_metadata = {
        "name": "New Document",
        "mimeType": "application/vnd.google-apps.document",
    }

    file = client.files().create(body=file_metadata).execute()

    # When using a service account, granting access to a specific user
    # can simplify file interactions. This step is optional.
    if USER_EMAIL:
        client.permissions().create(
            fileId=file.get("id"),
            body={"type": "user", "role": "writer", "emailAddress": USER_EMAIL},
        ).execute()

    print(f"Created file with ID: {file.get('id')}")

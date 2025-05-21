"""Download a file via SFTP, remove spaces and upload it."""

from io import BytesIO
import os

import autokitteh
import paramiko
import requests


SFTP_CONFIG = {
    "host": "test.rebex.net",
    "port": 22,
    "username": "demo",
    "password": "password",
    "remote_path": "/readme.txt",
}


HTTP_TARGET = os.getenv("HTTP_TARGET")


def download_sftp_file(host, port, username, password, remote_path):
    transport = paramiko.Transport((host, port))
    transport.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(transport)

    file_io = BytesIO()
    sftp.getfo(remote_path, file_io)
    file_io.seek(0)

    sftp.close()
    transport.close()
    return file_io


def remove_spaces(file_io):
    content = file_io.read().decode("utf-8").replace(" ", "")
    return BytesIO(content.encode("utf-8"))


def send_file_http(file_io, filename, url):
    file_io.seek(0)
    files = {"file": (filename, file_io)}
    response = requests.post(url, files=files, timeout=10)
    return response.status_code, response.text


# Use a single activity to avoid Temporal's data serialization between steps.
# - big files boundary.
# - Keeps a stream (not serializable) in-process.
@autokitteh.activity
def on_webhook_call(_):
    """Download a file via SFTP, remove spaces and upload it."""
    print("Downloading from SFTP...")
    file_io = download_sftp_file(**SFTP_CONFIG)

    processed = remove_spaces(file_io)

    print(f"Sending to {HTTP_TARGET}...")
    status, msg = send_file_http(processed, "readme.txt", HTTP_TARGET)
    print(f"Upload status: {status}, Message: {msg}")

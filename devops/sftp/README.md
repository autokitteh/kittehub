---
title: SFTP demo
description: Trigger a file transfer from SFTP to HTTP on webhook call
integrations: ["http"]
categories: ["DevOps"]
---

# SFTP demo

[![Start with AutoKitteh](https://autokitteh.com/assets/autokitteh-badge.svg)](https://app.autokitteh.cloud/template?name=devops/sftp)

This project listens for webhook events and automatically transfers a file from an SFTP server to an HTTP endpoint. It removes spaces from the file content before sending. The goal is to provide a lightweight, event-driven integration point between two systems.

## How It Works

1. The workflow is triggered by a HTTP request.
2. Connects to a remote SFTP server and downloads a specific file.
3. Removes all spaces from the file contents.
4. Sends the cleaned file to a predefined HTTP endpoint.

## Cloud Usage (Recommended)

1. Set the `HTTP_TARGET` environment variable to your HTTP endpoint in the "VARIABLES" tab
2. Copy the webhook URLs from the "Triggers" tab (see the [instructions here](https://docs.autokitteh.com/get_started/deployment#webhook-urls))
3. Deploy the project

## Trigger Workflow

Send HTTP request to the webhook URL from step 2 in the [Cloud Usage](#cloud-usage) section above.

> [!NOTE]
> Make sure the remote SFTP server is accessible and the credentials are correct. This project uses `paramiko` for SFTP and `requests` for HTTP.

## Configuration

Update the `SFTP_CONFIG` dictionary in the source code to match your SFTP server details:

```python
SFTP_CONFIG = {
    "host": "your.sftp.host",
    "port": 22,
    "username": "your_username",
    "password": "your_password",
    "remote_path": "/path/to/file.txt"
}
```

## Self-Hosted Deployment

Follow [these detailed instructions](https://docs.autokitteh.com/get_started/deployment) to deploy the project on a self-hosted server.

---
title: Google Sheets Notifications
description: detects and responds to changes in Google Sheets documents
integrations: ["googledrive"]
categories: ["Productivity", "Reliability"]
tags: ["google sheets events", "file_monitoring", "notifications"]
---

# Google Sheets Notifications

This project detects when Google Sheets documents are edited and processes those change events.

This project monitors spreadsheet change by integrating Google Drive to track file modifications and filter for Google Sheets documents specifically.

API documentation:

- Google Drive: https://docs.autokitteh.com/integrations/google/drive

## How It Works

1. Monitor Google Drive for file change events
2. Filter events to only include Google Sheets documents
3. Process spreadsheet change notifications
4. Log the file ID and change details

## Cloud Usage

1. Initialize your connection (Google Drive)
2. Deploy project

## Trigger Workflow

> [!IMPORTANT]
> Ensure all connections (Google Drive) are initialized; otherwise, the workflow will raise a `ConnectionInitError`.

The workflow is triggered via Google Drive when files are modified. The system filters these events to only process changes to Google Sheets documents.

## Self-Hosted Deployment

Follow [these detailed instructions](https://docs.autokitteh.com/get_started/deployment) to deploy the project on a self-hosted server.

## Known Limitations

- Only change events for files created by or explicitly shared with the app are triggered when using the `drive.file` scope.
- Does not track creation or deletion of spreadsheets

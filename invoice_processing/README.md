---
title: Invoice processing system
description: Process emails for invoices, extract data, and generate reports
integrations: ["gmail", "chatgpt"]
categories: ["AI", "Productivity"]
---

# Invoice Processing System

[![Start with AutoKitteh](https://autokitteh.com/assets/autokitteh-badge.svg)](https://app.autokitteh.cloud/template?name=invoice_processing)

Automate the detection and extraction of invoices from emails using Gmail and ChatGPT. This system scans incoming emails, identifies invoices, extracts key details, and generates structured reports.

## How It Works

1. Fetch new emails from Gmail API
2. Identify whether the email contains an invoice using ChatGPT
3. Extract invoice details such as company name, date, amount, and invoice ID
4. Generate structured JSON output
5. Send invoice reports to the user

## Cloud Usage

1. Initialize your connections (Gmail, ChatGPT)
2. Set the `POLLING_INTERVAL_MINUTES` and the `START_DATE` project variables to define the polling frequency and the start date for processing
3. Deploy the project

> [!NOTE]
> Use the date format specified in [Google's DateTime Formatting Guide](https://developers.google.com/gmail/markup/reference/datetime-formatting)

## Trigger Workflow

> [!IMPORTANT]
> Ensure all connections (Gmail, ChatGPT) are properly initialized before the workflow starts running.

1. Start the workflow by calling the `process_invoices` webhook URL:
   ```shell
   curl -i "${WEBHOOK_URL}"
   ```
2. Send yourself an email containing an invoice by calling `send_mail` webhook URL:
   ```shell
   curl -i "${WEBHOOK_URL}"
   ```

> [!TIP]
> The program workflow can also be triggered manually by clicking the "Run" button in the UI, and choosing the `program.py` file and setting the `main` function as the entry point.

## Self-Hosted Deployment

Follow [these detailed instructions](https://docs.autokitteh.com/get_started/deployment) to deploy the project on a self-hosted server.

## Known Limitations

- AI Accuracy: Results can be inconsistent because the email content is processed through the OpenAI API. Sometimes it can accurately detect details like the company name and price, while other times it may miss certain information.

- Email Polling: The polling mechanism may not detect all cases instantly.

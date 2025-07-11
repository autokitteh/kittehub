---
title: Google Sheets to SOAP Calculator
description: Reads numeric values from Google Sheets and sends them to a SOAP-based calculator API
integrations: ["sheets"]
categories: ["Productivity", "DevOps"]
tags: ["webhook_handling", "data_processing", "notifications"]
---

# Google Sheets to SOAP Calculator

This AutoKitteh project demonstrates how to integrate Google Sheets with a SOAP-based calculator service. It reads values from a Google Sheet and sends them to the SOAP service to perform addition.

## API Documentation

- [Google Sheets API](https://docs.autokitteh.com/integrations/google/sheets/python)
- [SOAP Calculator WSDL](http://www.dneonline.com/calculator.asmx?WSDL)

## How It Works

1. Reads pairs of numeric values (columns A and B)
2. Sends each pair to a public SOAP API for addition
3. Prints the result of each addition in the logs

## Cloud Usage

1. Initialize your Google Sheets connection

2. Set the SHEET_RANGE and SHEET_ID project variables. You can optionally set the SOAP_WSDL project variable

3. Copy the webhook URL from the "Triggers" tab (see the [instructions here](https://docs.autokitteh.com/get_started/deployment#webhook-urls))

4. Deploy project

## Trigger Workflow

Start an AutoKitteh session by sending an HTTP GET request to the webhook URL from step 3 in the [Cloud Usage](#cloud-usage) section above:

```shell
curl -i "${WEBHOOK_URL}"
```

> [!TIP]
> The workflow can also be triggered manually by clicking the "Run" button in the UI.

## Self-Hosted Deployment

Follow [these detailed instructions](https://docs.autokitteh.com/get_started/deployment) to deploy the project on a self-hosted server.

---
title: Google Forms sample
description: Samples using Google Forms APIs
integrations: ["forms"]
categories: ["Samples"]
---

# Google Forms Sample

[![Start with AutoKitteh](https://autokitteh.com/assets/autokitteh-badge.svg)](https://app.autokitteh.cloud/template?name=samples/google/forms)

This AutoKitteh project demonstrates 2-way integration with
[Google Forms](https://www.google.com/forms/about/).

It appends questions to a form, and handles two event types: form changes
(a.k.a. `schema`) and form responses (a.k.a. `responses`).

API Documentation:

- https://docs.autokitteh.com/integrations/google/forms/python
- https://docs.autokitteh.com/integrations/google/forms/events

## How It Works

- Monitor Form Activity - Watch a Google Form for changes and new responses
- Process Form Events - Handle form updates and submission events
- Modify Form Content - Programmatically add new questions to the form

> [!IMPORTANT]
> Specify the ID of a form that you own, to receive notifications about it.

## Cloud Usage

1. Initialize your connection with Google Forms (make sure to specify the ID of a form that you own, to receive notifications about it)
2. Copy the webhook URL from the "Triggers" tab (see the [instructions here](https://docs.autokitteh.com/get_started/deployment#webhook-urls))
3. Deploy project

## Trigger Workflow

- Start a long-running AutoKitteh session by sending an HTTP GET request to the webhook URL from step 2 in the [Cloud Usage](#cloud-usage) section above:

  ```shell
  curl -i "${WEBHOOK_URL}"
  ```

- Edit the Google Form - any changes will trigger the on_form_change event
- Submit a form response - will trigger the on_form_response event

## Self-Hosted Deployment

Follow [these detailed instructions](https://docs.autokitteh.com/get_started/deployment) to deploy the project on a self-hosted server.

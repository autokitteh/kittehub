---
title: Twilio sample
description: Samples using Twilio APIs
integrations: ["twilio"]
categories: ["Samples"]
---

# Twilio Sample

[![Start with AutoKitteh](https://autokitteh.com/assets/autokitteh-badge.svg)](https://app.autokitteh.cloud/template?name=samples/twilio)

This sample project demonstrates AutoKitteh's integration with
[Twilio](https://www.twilio.com).

API documentation:

- [Messaging API overview](https://www.twilio.com/docs/messaging/api)
- [Voice API overview](https://www.twilio.com/docs/voice/api)

## Cloud Usage

1. Initialize your Twilio connection
2. Copy the webhook URL from the "Triggers" tab (see the [instructions here](https://docs.autokitteh.com/get_started/deployment#webhook-urls))
3. Set the `FROM_PHONE_NUMBER` project variable
4. Deploy project

## Trigger Workflow

> [!IMPORTANT]
> Ensure your Twilio connection is initialized; otherwise, the workflow will raise a `ConnectionInitError`.

- Send an HTTP GET request to the webhook URL from step 3 in the [Cloud Usage](#cloud-usage) section above:

```shell
curl -i "${WEBHOOK_URL}"
```

## Self-Hosted Deployment

Follow [these detailed instructions](https://docs.autokitteh.com/get_started/deployment) to deploy the project on a self-hosted server.

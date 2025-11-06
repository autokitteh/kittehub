---
title: Runtime Events sample
description: Samples using events in AutoKitteh - subscribe(), next_event(), unsubscribe()
integrations: []
categories: ["Samples"]
tags:
  [
    "subscribe",
    "next_event",
    "unsubscribe",
    "event_filtering",
    "timeout_handling",
    "essential",
  ]
---

# Runtime Event Handling Sample

[![Start with AutoKitteh](https://autokitteh.com/assets/autokitteh-badge.svg)](https://app.autokitteh.cloud/template?template-name=samples/runtime_events)

[The workflow](./program.py) is triggered by an HTTP GET request with a URL
path that ends with `/meow`.

During runtime, it waits (up to 1 minute) for a subsequent webhook event
where the URL path ends with `/woof`.

For detailed information about runtime event subscriptions, see:
https://docs.autokitteh.com/develop/events/subscription

## Cloud Usage

1. Copy the webhook URL from the "Triggers" tab (see the [instructions here](https://docs.autokitteh.com/get_started/deployment#webhook-urls))
2. Deploy the project

## Trigger Workflow

1. Run this command to start a session:

   ```shell
   curl -i "${WEBHOOK_URL}/meow"
   ```

2. Run this command to end the session:

   ```shell
   curl -i "${WEBHOOK_URL}/woof"
   ```

3. Repeat step 1, but this time wait a minute until the session times out

4. Check out the resulting session logs in the AutoKitteh server for each of
   the steps above

## Self-Hosted Deployment

Follow [these detailed instructions](https://docs.autokitteh.com/get_started/deployment) to deploy the project on a self-hosted server.

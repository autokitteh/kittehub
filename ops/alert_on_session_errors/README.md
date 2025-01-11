---
title: Alert on session errors
description: Send Slack alerts when AutoKitteh sessions end due to errors
integrations: ["Slack"]
categories: ["Ops"]
---

# Alert on Session Errors

Send Slack alerts when AutoKitteh sessions end due to errors.

This is a detection tool for incidents due to unexpected exceptions
in workflows that are usually stable and dependable. It can also be
used as a development and debugging tool.

It gets triggered by the AutoKitteh scheduler every minute, on the minute,
to look for sessions that ended with an error status in the previous minute.

## Configuration and Deployment

### Cloud Usage

1. Generate a personal API auth token in the web UI:

   - Click your user icon in the bottom-left corner of the page
   - Click the "Client Setup" menu option to go to that page
   - Click the "Generate Token" button, and copy the generated
     [JWT](https://jwt.io/)

2. Import/upload the project
3. Initialize your connections
4. Set/modify these project variables:

   - `AUTOKITTEH_API_BASE_URL` (default = `https://api.autokitteh.cloud`,
     use `http://localhost:9980` for self-hosted servers)
   - `AUTOKITTEH_UI_BASE_URL` (default = `https://app.autokitteh.cloud`,
     use `http://localhost:9982` for self-hosted servers)
   - `AUTOKITTEH_AUTH_TOKEN`: the API auth token generated in step 1 above
   - `SLACK_CHANNEL`: send alert messages to this Slack channel name/ID
     (default = `autokitteh-alerts`)

5. Deploy the project

### Self-Hosted Usage

Generate a personal API auth token, by running this CLI command:

```shell
ak auth create-token
```

Follow [these detailed instructions](https://docs.autokitteh.com/get_started/deployment)
to deploy the project on a self-hosted server.

Also follow steps 3-4 in the [Cloud Usage](#cloud-usage) section above.

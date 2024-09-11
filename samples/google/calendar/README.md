# Google Calendar Sample

This AutoKitteh project demonstrates 2-way integration with
[Google Calendar](https://workspace.google.com/products/calendar/).

## API Documentation

- https://docs.autokitteh.com/integrations/google/calendar/python
- https://docs.autokitteh.com/integrations/google/calendar/events

## Setup Instructions

1. Install and start a
   [self-hosted AutoKitteh server](https://docs.autokitteh.com/get_started/quickstart),
   or use AutoKitteh Cloud

2. Optional for self-hosted servers (preconfigured in AutoKitteh Cloud): \
   [enable Google connections to use OAuth 2.0](https://docs.autokitteh.com/integrations/google/config)

> [!NOTE]
> No need to configure GCP Cloud Pub/Sub for this sample - only the Gmail and
> Google Forms integrations require it.

3. Run these commands to deploy this project's manifest file:

   ```shell
   git clone https://github.com/autokitteh/kittehub.git
   ak deploy --manifest kittehub/samples/google/calendar/autokitteh.yaml
   ```

4. Look for the following line in the output of the `ak deploy` command, and
   copy the URL path for later:

   ```
   [!!!!] trigger "list_events" created, webhook path is "/webhooks/..."
   ```

> [!TIP]
> If you don't see the output of `ak deploy` anymore, you can run this command
> instead, and use the webhook slug from the output:
>
> ```shell
> ak trigger get list_events --project google_calendar_sample -J
> ```

5. Initialize this project's Google Calendar connection, with user
   impersonation using OAuth 2.0 (based on step 2), or a GCP service account's
   JSON key

> [!TIP]
> The exact CLI command to do so (`ak connection init ...`) will appear in the
> output of the `ak deploy` command from step 3 when you create the project on
> the server, i.e. when you run that command for the first time.

> [!IMPORTANT]
> Specify the ID of a calendar that you own (e.g. `primary`), to receive
> notifications about it.

## Usage Instructions

Outgoing API calls:

1. Run this command to start a session that lists the next 10 calendar events
   (use the URL path from step 4 above instead of `/webhooks/...`):

   ```shell
   curl -i "http://localhost:9980/webhooks/..."
   ```

2. Check out the resulting session log in the AutoKitteh server

Incoming events:

1. Create/edit/delete
   [Google Calendar events](https://developers.google.com/calendar/api/guides/event-types)

2. Check out the resulting session logs in the AutoKitteh server

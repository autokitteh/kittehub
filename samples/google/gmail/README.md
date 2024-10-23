
# Gmail Sample

This AutoKitteh project demonstrates 2-way integration with
[Gmail](https://www.google.com/gmail/about/).

## API Documentation

- https://docs.autokitteh.com/integrations/google/gmail/python
- https://docs.autokitteh.com/integrations/google/gmail/events

## Setup Instructions

1. Install and start a
   [self-hosted AutoKitteh server](https://docs.autokitteh.com/get_started/quickstart),
   or use AutoKitteh Cloud.

2. Optional for self-hosted servers (preconfigured in AutoKitteh Cloud):

   - [Enable Google connections to use OAuth 2.0](https://docs.autokitteh.com/integrations/google/config)

3. Run these commands to deploy this project's manifest file:

   ```shell
   git clone https://github.com/autokitteh/kittehub.git
   ak deploy --manifest kittehub/samples/google/gmail/autokitteh.yaml
   ```

4. Initialize this project's connections:

   - Gmail: with user impersonation using OAuth 2.0 (based on step 2),
     or a GCP service account's JSON key.

> [!TIP]
> The exact CLI commands to do so (`ak connection init ...`) will appear in
> the output of the `ak deploy` command from step 3 when you create the
> project on the server, i.e., when you run that command for the first time.

## Usage Instructions

1. Run these commands to interact with Gmail via HTTP trigger using query parameters:

   ```shell
   curl -i "http://localhost:9980/webhooks/SLUG?cmd=get_profile"
   curl -i "http://localhost:9980/webhooks/SLUG?cmd=list_drafts&query=optional_query"
   curl -i "http://localhost:9980/webhooks/SLUG?cmd=get_draft&draft_id=<draft_ID>"
   curl -i "http://localhost:9980/webhooks/SLUG?cmd=list_messages&query=optional_query"
   curl -i "http://localhost:9980/webhooks/SLUG?cmd=get_message&message_id=<message_ID>"
   curl -i "http://localhost:9980/webhooks/SLUG?cmd=send_message&text=<message_text>"
   ```

2. View the responses in your terminal after making the requests.

# Gmail Sample

This AutoKitteh project demonstrates 2-way integration with
[Gmail](https://www.google.com/gmail/about/).

## API Documentation

- https://docs.autokitteh.com/integrations/google/gmail/python
- https://docs.autokitteh.com/integrations/google/gmail/events

## Setup Instructions

1. Install and start a
   [self-hosted AutoKitteh server](https://docs.autokitteh.com/get_started/quickstart),
   or use AutoKitteh Cloud

2. Optional for self-hosted servers (preconfigured in AutoKitteh Cloud):

   - [Enable Google connections to use OAuth 2.0](https://docs.autokitteh.com/integrations/google/config)
   - [Enable Slack connections to use an OAuth v2 app](https://docs.autokitteh.com/integrations/slack/config)

3. Run these commands to deploy this project's manifest file:

   ```shell
   git clone https://github.com/autokitteh/kittehub.git
   ak deploy --manifest kittehub/samples/google/gmail/autokitteh.yaml
   ```

4. Initialize this project's connections:

   - Google Sheets: with user impersonation using OAuth 2.0 (based on step 2),
     or a GCP service account's JSON key
   - Slack: with an OAuth v2 app (based on step 2), or a Socket Mode app

> [!TIP]
> The exact CLI commands to do so (`ak connection init ...`) will appear in
> the output of the `ak deploy` command from step 3 when you create the
> project on the server, i.e. when you run that command for the first time.

## Usage Instructions

1. Run a slash command of the Slack app that you initialized in step 4 above,
   with any of these commands as the slash command's text:

   - `gmail get profile`
   - `gmail drafts list [optional query]`
   - `gmail drafts get <draft ID>`
   - `gmail messages list [optional query]`
   - `gmail messages get <message ID>`
   - `gmail messages send <short message to yourself>`

2. See the Slack app's DM responses to you

3. Send to yourself an email, using the Slack slash command with this text:

   ```
   gmail messages send <Slack channel name or ID>
   ```

4. See the resulting message in the specified Slack channel - which is a
   result of handling a mailbox change event from Gmail

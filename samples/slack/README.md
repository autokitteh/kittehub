# Slack Sample

This sample project demonstrates AutoKitteh's 2-way integration with
[Slack](https://slack.com).

The code file ([`program.py`](./program.py) implements multiple entry-point
functions that are triggered by incoming Slack events, as defined in the
[`autokitteh.yaml`](./autokitteh.yaml) manifest file. These functions also
execute various Slack API calls.

Slack API documentation:

- [Web API reference](https://api.slack.com/methods)
- [Events API reference](https://api.slack.com/events?filter=Events)
- [Python client API](https://slack.dev/python-slack-sdk/api-docs/slack_sdk/)

This project isn't meant to cover all available functions and events. It
merely showcases a few illustrative, annotated, reusable examples.

## Instructions

1. Deploy the manifest file:

   ```shell
   ak deploy --manifest samples/slack/autokitteh.yaml
   ```

2. Follow the instructions in the `ak` CLI tool's output:

   ```
   Connection created, but requires initialization.
   Please run this to complete:

   ak connection init <connection ID>
   ```

3. Events that this sample project responds to:

   - Mentions of the Slack app in messages (e.g. `Hi @autokitteh`)
   - Slash commands registered by the Slack app
     (`/autokitteh <channel name or ID>`)
   - New and edited messages and replies
   - New emoji reactions

## Connection Notes

AutoKitteh supports 2 connection modes:

- Slack app that uses
  [OAuth v2](https://docs.autokitteh.com/integrations/slack/config)

- Slack app that uses
  [Socket Mode](https://docs.autokitteh.com/integrations/slack/connection)

In both cases, the user authorizes the Slack app in step 3 above.

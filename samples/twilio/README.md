# Twilio Sample

This sample project demonstrates AutoKitteh's integration with
[Twilio](https://www.twilio.com).

The file [`program.py`](./program.py) implements a single entry-point function
triggered by a webhook event, as defined in the
[`autokitteh.yaml`](./autokitteh.yaml) manifest. This function initiates sending Twilio messages.

API details:

- [Messaging API overview](https://www.twilio.com/docs/messaging/api)
- [Voice API overview](https://www.twilio.com/docs/voice/api)

It also demonstrates using constant values which are set for each AutoKitteh
environment in the [`autokitteh.yaml`](./autokitteh.yaml) manifest file.

## Instructions

1. Set the `FROM_PHONE_NUMBER` environment value

2. Via the `ak` CLI tool, or the AutoKitteh VS Code extension, deploy the
   `autokitteh.yaml` manifest file

## Connection Notes

AutoKitteh supports connecting to Twilio using either an auth token or an
[API key](https://www.twilio.com/docs/glossary/what-is-an-api-key), which can
be configured in the AutoKitteh WebUI.

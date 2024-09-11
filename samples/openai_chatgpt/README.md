# OpenAI ChatGPT Sample

This [AutoKitteh](https://github.com/autokitteh/autokitteh) project
demonstrates integration with [ChatGPT](https://chat.openai.com).

The file [`program.star`](./program.star) implements a single entry-point
function, which is configured in the [`autokitteh.yaml`](./autokitteh.yaml)
manifest file as the receiver of Slack `slash_command` events.

It sends a couple of requests to the ChatGPT API, and sends the responses
back to the user over Slack, as well as ChatGPT token usage stats.

API details:

- [OpenAI developer platform](https://platform.openai.com/)
- [Go client API](https://pkg.go.dev/github.com/sashabaranov/go-openai)

This project isn't meant to cover all available functions and events. it
merely showcases a few illustrative, annotated, reusable examples.

## Instructions

1. Follow instructions [here](https://platform.openai.com/docs/quickstart) to setup your OpenAI API account.

2. Via the `ak` CLI tool, or the AutoKitteh WebUI, initialize the OpenAI connection and provide API key generated in step 1. 

3. Via the `ak` CLI tool, or the AutoKitteh VS Code extension, deploy the
   `autokitteh.yaml` manifest file

# OpenAI ChatGPT Sample

This [AutoKitteh](https://github.com/autokitteh/autokitteh) project
demonstrates integration with [ChatGPT](https://chat.openai.com).

The file [`program.py`](./program.py) implements a single entry-point
function, which is configured in the [`autokitteh.yaml`](./autokitteh.yaml)
manifest file as the receiver of HTTP events.

It sends a couple of requests to the ChatGPT API, and prints the responses
back to the user, as well as ChatGPT token usage stats.

API details:

- [OpenAI developer platform](https://platform.openai.com/)
- [Python client API](https://github.com/openai/openai-python)

This project isn't meant to cover all available functions and events. It
merely showcases a few illustrative, annotated, reusable examples.

## Instructions

1. Follow instructions [here](https://platform.openai.com/docs/quickstart) to set up your OpenAI API account.

2. Via the `ak` CLI tool, or the AutoKitteh WebUI, initialize the OpenAI connection and provide the API key generated in step 1.

3. Via the `ak` CLI tool, or the AutoKitteh VS Code extension, deploy the `autokitteh.yaml` manifest file.

4. Once deployed, the program is ready to receive HTTP POST requests. You can test the program by sending a POST request to the endpoint as shown below:

   ```shell
   curl -X POST "http://localhost:9980/webhooks/<webhook_slug>" -H "Content-Type: text/plain" -d "Meow"
   ```

5. You can modify the request body in the curl command to send custom text and observe how ChatGPT responds with dynamic content.

> [!NOTE]
> The [`autokitteh.yaml`](autokitteh.yaml) manifest file is set up to filter incoming HTTP requests. You can modify or remove this filter as needed.

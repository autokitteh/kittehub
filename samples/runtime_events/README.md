# Runtime Event Handling Sample

[The workflow](./program.py) is triggered by an HTTP GET request with a URL
path that ends with `/meow`. The trigger is defined in the
[autokitteh.yaml](./autokitteh.yaml) manifest file.

During runtime, it waits (up to 1 minute) for a subsequent webhook event
where the URL path ends with `/woof`, using the `subscribe` and `get_event`
functiona in the AutoKitteh Python SDK.

For detailed information about runtime event subscriptions, see:
https://docs.autokitteh.com/develop/events/subscription

## Setup Instructions

1. Install and start a
   [self-hosted AutoKitteh server](https://docs.autokitteh.com/get_started/quickstart),
   or use AutoKitteh Cloud

2. Run these commands to deploy this project's manifest file:

   ```shell
   git clone https://github.com/autokitteh/kittehub.git
   ak deploy --manifest kittehub/samples/runtime_events/autokitteh.yaml
   ```

3. Look for the following line in the output of the `ak deploy` command, and
   copy the URL path for later:

   ```
   [!!!!] trigger "meow_webhook" created, webhook path is "/webhooks/..."
   ```

> [!TIP]
> If you don't see the output of `ak deploy` anymore, you can run this command
> instead, and use the webhook slug from the output:
>
> ```shell
> ak trigger get meow_webhook --project runtime_events_sample -J
> ```

## Usage Instructions

1. Run this command to start a session (use the URL path from step 3 above
   instead of `/webhooks/...`, and append `meow` to it):

   ```shell
   curl -i "http://localhost:9980/webhooks/.../meow"
   ```

2. Run this command to end the session (use the same URL path, but this time
   append `woof` to it instead of `meow`):

   ```shell
   curl -i "http://localhost:9980/webhooks/.../woof"
   ```

3. Repeat step 1, but this time wait a minute until the session times out

4. Check out the resulting session logs in the AutoKitteh server for each of
   the steps above

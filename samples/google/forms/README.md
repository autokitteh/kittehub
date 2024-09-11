# Google Forms Sample

This AutoKitteh project demonstrates 2-way integration with
[Google Forms](https://www.google.com/forms/about/).

It appends questions to a form, and handles two event types: form changes
(a.k.a. `schema`) and form responses (a.k.a. `responses`).

## API Documentation

- https://docs.autokitteh.com/integrations/google/forms/python
- https://docs.autokitteh.com/integrations/google/forms/events

## Setup Instructions

1. Install and start a
   [self-hosted AutoKitteh server](https://docs.autokitteh.com/get_started/quickstart),
   or use AutoKitteh Cloud

2. Optional for self-hosted servers (preconfigured in AutoKitteh Cloud): \
   [enable Google connections to use OAuth 2.0](https://docs.autokitteh.com/integrations/google/config)

3. Run these commands to deploy this project's manifest file:

   ```shell
   git clone https://github.com/autokitteh/kittehub.git
   ak deploy --manifest kittehub/samples/google/forms/autokitteh.yaml
   ```

4. Look for the following line in the output of the `ak deploy` command, and
   copy the URL path for later:

   ```
   [!!!!] trigger "add_question" created, webhook path is "/webhooks/..."
   ```

> [!TIP]
> If you don't see the output of `ak deploy` anymore, you can run this command
> instead, and use the webhook slug from the output:
>
> ```shell
> ak trigger get add_question --project google_forms_sample -J
> ```

5. Initialize this project's Google Forms connection, with user impersonation
   using OAuth 2.0 (based on step 2), or a GCP service account's JSON key

> [!TIP]
> The exact CLI command to do so (`ak connection init ...`) will appear in the
> output of the `ak deploy` command from step 3 when you create the project on
> the server, i.e. when you run that command for the first time.

> [!IMPORTANT]
> Specify the ID of a form that you own, to receive notifications about it.

## Usage Instructions

1. Run this command to start a session that appends a question to the form
   watched by the Google Forms connection (use the URL path from step 4
   above instead of `/webhooks/...`):


   ```shell
   curl -i "http://localhost:9980/webhooks/..."
   ```

2. The session in step 1 will cause Google Forms to send a form-change event
   (a.k.a. `schema`) to the AutoKitteh server, which will start another session

3. Check out both session logs in the AutoKitteh server:

   - The first one, triggered by the HTTP request
   - The second one, triggered by the subsequent Google Forms event

4. Submit a response to the form - this will cause Google Forms to send a
   new-response event (a.k.a. `responses`) to the AutoKitteh server, which
   will start a third session

5. Check out the resulting session log in the AutoKitteh server

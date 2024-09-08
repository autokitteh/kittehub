# Google Forms to Jira

This project creates Jira issues based on Google Forms responses.

## How It Works

1. The workflow is triggered by response events from Google Forms, for a
   specific form ID

2. The workflow extracts the answers from the response, and matches them with
   the form's questions, to construct a human-readable summary

3. The workflow checks if there's already an existing Jira issue for the
   response's ID:

   - No (new response): it creates a new Jira issue
   - Yes (edited response): it updates the existing Jira issue's description
     with the new response

## API Documentation

Atlassian Jira:

- https://docs.autokitteh.com/integrations/atlassian/jira/python
- https://docs.autokitteh.com/integrations/atlassian/jira/events

Google Forms:

- https://docs.autokitteh.com/integrations/google/forms/python
- https://docs.autokitteh.com/integrations/google/forms/events

## Setup Instructions

1. Install and start a
   [self-hosted AutoKitteh server](https://docs.autokitteh.com/get_started/quickstart),
   or use AutoKitteh Cloud

2. Optional for self-hosted servers (preconfigured in AutoKitteh Cloud):

   - [Enable Google connections to use OAuth 2.0](https://docs.autokitteh.com/integrations/google/config)
   - [Enable Atlassian connections to use an OAuth 2.0 (3LO) app](https://docs.autokitteh.com/integrations/atlassian/config)

3. Run this command to clone the Kittehub repository, which contains this
   project:

   ```shell
   git clone https://github.com/autokitteh/kittehub.git
   ```

4. Set the `JIRA_PROJECT_KEY` variable in this project's
   [autokitteh.yaml](./autokitteh.yaml) manifest file

5. Run this command to deploy this project's manifest file:

   ```shell
   ak deploy --manifest kittehub/google_forms_to_jira/autokitteh.yaml
   ```

6. Initialize this project's connections:

   - Atlassian Jira: with an OAuth 2.0 (3LO) app (based on step 2), or with
     user impersonation using an API token or a Personal Access Token (PAT)
   - Google Forms: with user impersonation using OAuth 2.0 (based on step 2),
     or a GCP service account's JSON key

> [!TIP]
> The exact CLI commands to do so (`ak connection init ...`) will appear in
> the output of the `ak deploy` command from step 3 when you create the
> project on the server, i.e. when you run that command for the first time.

> [!IMPORTANT]
> Specify the ID of a form that you own, to receive notifications about it.

## Usage Instructions

1. Run this command to start a session that appends a question to the form
   watched by the Google Forms connection (use the URL path from step 4
   above instead of `/webhooks/.../`):

   ```shell
   curl -iL "http://localhost:9980/webhooks/.../"
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

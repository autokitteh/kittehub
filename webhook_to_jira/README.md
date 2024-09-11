# Webhook to Jira

This project creates Jira issue based on various HTTP requests:

- HTTP GET with query parameters
- HTTP POST with a URL-encoded form body
- HTTP POST with a JSON body

This is particularly useful when you need to create issues automatically from
another system or service with no fuss.

## API Documentation

Atlassian Jira:

- https://docs.autokitteh.com/integrations/atlassian/jira/python

HTTP:

- https://docs.autokitteh.com/integrations/http/events

## Setup Instructions

1. Install and start a
   [self-hosted AutoKitteh server](https://docs.autokitteh.com/get_started/quickstart),
   or use AutoKitteh Cloud

2. Optional for self-hosted servers (preconfigured in AutoKitteh Cloud): \
   [enable Atlassian connections to use an OAuth 2.0 (3LO) app](https://docs.autokitteh.com/integrations/atlassian/config)

3. Run these commands to deploy this project's manifest file:

   ```shell
   git clone https://github.com/autokitteh/kittehub.git
   ak deploy --manifest kittehub/webhook_to_jira/autokitteh.yaml
   ```

4. Look for the following line in the output of the `ak deploy` command, and
   copy the URL path for later:

   ```
   [!!!!] trigger "http_get_or_post_request" created, webhook path is "/webhooks/..."
   ```

> [!TIP]
> If you don't see the output of `ak deploy` anymore, you can run this command
> instead, and use the webhook slug from the output:
>
> ```shell
> ak trigger get http_get_or_post_request --project webhook_to_jira -J
> ```

5. Initialize this project's Atlassian Jira connection, with an OAuth 2.0
   (3LO) app (based on step 3), or with user impersonation using a token

> [!TIP]
> The exact CLI command to do so (`ak connection init ...`) will appear in the
> output of the `ak deploy` command from step 3 when you create the project on
> the server, i.e. when you run that command for the first time.

## Usage Instructions

> [!TIP]
> Steps 1 and 2 are limited to simple fields, but the JSON payload in step 3
> may contain [any field that Jira's REST API supports](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issues/#api-rest-api-3-issue-post-request-body).

1. Run this command to create a Jira issue using an HTTP GET request with
   URL-encoded query parameters (use the URL path from step 4 above instead of
   `/webhooks/...`):

   ```shell
   curl -i [--get] "http://localhost:9980/webhooks/..." \
        --url-query project=TEST --url-query issuetype=Task \
        --url-query "summary=Test issue 1" \
        --url-query "description=Created with HTTP GET" \
   ```

2. Run this command to create a Jira issue using an HTTP POST request with a
   URL-encoded form body (use the URL path from step 4 above instead of
   `/webhooks/...`):

   ```shell
   curl -i [-X POST] "http://localhost:9980/webhooks/..." \
        --data project=TEST --data issuetype=Task \
        --data "summary=Test issue 2" \
        --data "description=Created with URL-encoded form" \
   ```

3. Run this command to create a Jira issue using an HTTP POST request with a
   JSON body (use the URL path from step 4 above instead of `/webhooks/...`):

   ```shell
   curl -i [-X POST] "http://localhost:9980/webhooks/..." \
        --json @file.json
   ```

   With this minimal content for `file.json`:

   ```json
   {
     "project": { "key": "TEST" },
     "issuetype": { "name": "Task" },
     "summary": "Test issue 3",
     "description": "Created with JSON"
   }
   ```

   As well as any other field from
   [Jira's REST API](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issues/#api-rest-api-3-issue-post-request-body).

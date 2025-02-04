---
title: HTTP sample
description: Samples using HTTP requests and webhooks
integrations: ["http"]
categories: ["Samples"]
---

# HTTP Sample

This AutoKitteh project demonstrates 2-way usage of HTTP, with AutoKitteh
webhooks and the Python [requests](https://requests.readthedocs.io/) library.

API Documentation:

- https://docs.autokitteh.com/integrations/http/python
- https://docs.autokitteh.com/integrations/http/events

## How It Works

1. Send Authenticated Requests - Makes HTTP requests with credentials using Basic Auth and Bearer Token
2. Test Authentication - Tests successful and failed authentication attempts
3. Display Results - Shows response codes, headers, and messages from the server

## Cloud Usage

1. Copy the webhook URLs from the "Triggers" tab (see the [instructions here](https://docs.autokitteh.com/get_started/deployment#webhook-urls))
2. Deploy the project

## Trigger Workflow

1. Run these commands to start sessions that receive GET and HEAD requests
   (use webhook `receive_http_get_or_head`):

   ```shell
   curl -i [--get] "${WEBHOOK_URL}"
   curl -i --head  "${WEBHOOK_URL}/SLUG1"
        [--url-query "key1=value1" --url-query "key2=value2"]
   ```

2. Run this command to start a session that parses a URL-encoded form in a
   POST request (use webhook `receive_http_post_form`):

   ```shell
   curl -i [-X POST] "${WEBHOOK_URL}/SLUG2" \
        --data key1=value1 --data key2=value2
   ```

3. Run this command to start a session that parses the JSON body of a POST
   request (use webhook `receive_http_post_json`):

   ```shell
   curl -i [-X POST] "${WEBHOOK_URL}/SLUG3" \
        --json '{"key1": "value1", "key2": "value2"}'
   ```

4. Run this command to start a session that sends various requests (use webhook `send_requests`):

   ```shell
   curl -i "${WEBHOOK_URL}/SLUG4"
   ```

   - Unauthenticated requests
     - GET: with query parameters, HTML body, JSON body, 404 not found
     - POST: URL-encoded form, JSON data
   - Requests with (correct and incorrect)
     [HTTP basic authentication](https://datatracker.ietf.org/doc/html/rfc7617)
   - Requests with an
     [OAuth bearer token](https://datatracker.ietf.org/doc/html/rfc6750)

5. Check out the resulting session logs in the AutoKitteh server for each of
   the steps above

## Self-Hosted Deployment

Follow [these detailed instructions](https://docs.autokitteh.com/get_started/deployment) to deploy the project on a self-hosted server.

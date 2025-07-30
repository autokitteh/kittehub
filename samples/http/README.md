---
title: HTTP sample
description: Samples using HTTP requests and webhooks
integrations: []
categories: ["Samples"]
---

# HTTP Sample

[![Start with AutoKitteh](https://autokitteh.com/assets/autokitteh-badge.svg)](https://app.autokitteh.cloud/template?name=samples/http)

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

Send HTTP GET and POST requests to the webhook URLs from step 2 in the [Cloud Usage](#cloud-usage) section above.

For `receive_http_get_or_head`:

```shell
curl -i [--get] "${WEBHOOK_URL}"
curl -i --head  "${WEBHOOK_URL}"
      [--url-query "key1=value1" --url-query "key2=value2"]
```

For `receive_http_post_form`:

```shell
curl -i [-X POST] "${WEBHOOK_URL}" \
      --data key1=value1 --data key2=value2
```

For `receive_http_post_json`:

```shell
curl -i [-X POST] "${WEBHOOK_URL}" \
      --json '{"key1": "value1", "key2": "value2"}'
```

For `send_requests`:

```shell
curl -i "${WEBHOOK_URL}"
```

- Unauthenticated requests
  - GET: with query parameters, HTML body, JSON body, 404 not found
  - POST: URL-encoded form, JSON data
- Requests with (correct and incorrect)
  [HTTP basic authentication](https://datatracker.ietf.org/doc/html/rfc7617)
- Requests with an
  [OAuth bearer token](https://datatracker.ietf.org/doc/html/rfc6750)

## Self-Hosted Deployment

Follow [these detailed instructions](https://docs.autokitteh.com/get_started/deployment) to deploy the project on a self-hosted server.

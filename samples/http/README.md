# HTTP Sample

This AutoKitteh project demonstrates 2-way usage of HTTP, with AutoKitteh
webhooks and the Python [requests](https://requests.readthedocs.io/) library.

## API Documentation

- https://docs.autokitteh.com/integrations/http/python
- https://docs.autokitteh.com/integrations/http/events

## Setup Instructions

1. Install and start a
   [self-hosted AutoKitteh server](https://docs.autokitteh.com/get_started/quickstart),
   or use AutoKitteh Cloud

2. Run these commands to deploy this project's manifest file:

   ```shell
   git clone https://github.com/autokitteh/kittehub.git
   ak deploy --manifest kittehub/samples/http/autokitteh.yaml
   ```

3. Look for the following lines in the output of the `ak deploy` command, and
   copy the URL paths for later:

   ```
   [!!!!] trigger "..." created, webhook path is "/webhooks/..."
   ```

> [!TIP]
> If you don't see the output of `ak deploy` anymore, you can run these
> commands instead, and use the webhook slugs from their outputs:
>
> ```shell
> ak trigger get receive_http_get_or_head --project http_sample -J
> ak trigger get receive_http_post_form --project http_sample -J
> ak trigger get receive_http_post_json --project http_sample -J
> ak trigger get send_requests --project http_sample -J
> ```

## Usage Instructions

1. Run these commands to start sessions that receive GET and HEAD requests
   (use the **1st** URL path from step 3 above):

   ```shell
   curl -i [--get] "http://localhost:9980/webhooks/SLUG1"
   curl -i --head  "http://localhost:9980/webhooks/SLUG1"
        [--url-query "key1=value1" --url-query "key2=value2"]
   ```

2. Run this command to start a session that parses a URL-encoded form in a
   POST request (use the **2nd** URL path from step 3 above):

   ```shell
   curl -i [-X POST] "http://localhost:9980/webhooks/SLUG2" \
        --data key1=value1 --data key2=value2
   ```

3. Run this command to start a session that parses the JSON body of a POST
   request (use the **3rd** URL path from step 3 above):

   ```shell
   curl -i [-X POST] "http://localhost:9980/webhooks/SLUG3" \
        --json '{"key1": "value1", "key2": "value2"}'
   ```

4. Run this command to start a session that sends various requests (use the
   **4th** URL path from step 3 above):

   ```shell
   curl -i "http://localhost:9980/webhooks/SLUG4"
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

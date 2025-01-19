---
title: Auth0
description: Simple usage of the Auth0 API
integrations: ["auth0"]
categories: ["Samples"]
---

# Auth0 Sample

The Auth0 sample demonstrates how to streamline user and role management using AutoKitteh's Auth0 integration.

This example showcases functionality to assign roles to users within Auth0 and retrieve insights into weekly user growth by querying newly created users.

API details:

-[Auth0 API](https://auth0-python.readthedocs.io/en/latest/readme_content.html)
-[Python AUTH0 library](https://github.com/auth0/auth0-python/blob/master/EXAMPLES.md#connections)

## How It Works

1. Assign Roles to Users: Automatically assign roles to users based on their IDs.
2. Fetch Weekly User Growth: Retrieve and display the number of new users created in the past week.

## Cloud Usage 

1. Initialize your connection with Auth0
2. Copy the webhook URL from the "Triggers" tab (see the [instructions here](https://docs.autokitteh.com/get_started/deployment#webhook-urls))
3. Update the `ROLE_ID` project variable with the `id` of the role you want to assign to the user, e.g., `rol_fstvQ1eysK5VTkKt`
4. Deploy the project

## Trigger Workflow

`assign_role`:

Send an HTTP POST request to the the webhook URL from step 2 in the [Cloud Usage](#cloud-usage) section above:

```shell
curl -X POST "https://api.autokitteh.cloud/webhooks/{your-webhook-slug}" \
-d user_id=<user_id>
```

`weekly_user_growth`:

Workflow is automatically triggered every week

[!TIP]
> The `weekly_user_growth` workflow can also be triggered manually by clicking the "Run" button in the UI, and setting the `weekly_user_growth` function as the entry point.

## Self-Hosted Deployment

Follow [these detailed instructions](https://docs.autokitteh.com/get_started/deployment) to deploy the project on a self-hosted server.

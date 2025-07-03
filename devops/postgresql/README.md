---
title: PostgreSQL connection
description: Project showing how to connect to PostgreSQL database
integrations: ["postgres"]
categories: ["DevOps"]
---

# PostgreSQL Sample

[![Start with AutoKitteh](https://autokitteh.com/assets/autokitteh-badge.svg)](https://app.autokitteh.cloud/template?name=samples/postgresql)

This AutoKitteh project demonstrates how to connect to a PostgreSQL database using the `psycopg2` library.

## How It Works

1. **Database Connection** - Establishes a connection to PostgreSQL using environment variables.
2. **Query Execution** - Executes a simple SELECT query on the users table.
3. **Result Display** - Prints the query results to the console.

## Cloud Usage (Recommended)

1. Copy the webhook URL from the "Triggers" tab
2. Update the database connection variables in the project variables
3. Copy the webhook URL from the "Triggers" tab (see the [instructions here](https://docs.autokitteh.com/get_started/deployment#webhook-urls))
4. Deploy the project

## Trigger Workflow

Send an HTTP request to the webhook URL from step 2 in the [Cloud Usage](#cloud-usage) section above:

```shell
curl -i "${WEBHOOK_URL}"
```

## Self-Hosted Deployment

Follow [these detailed instructions](https://docs.autokitteh.com/get_started/deployment) to deploy the project on a self-hosted server.

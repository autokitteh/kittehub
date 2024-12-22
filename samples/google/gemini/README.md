---
title: Gemini
description: Simple usage of the Gemini API
integrations: ["gemini"]
categories: ["Samples"]
---

# Gemini Sample

This [AutoKitteh](https://github.com/autokitteh/autokitteh) project
demonstrates integration with [Gemini](https://gemini.google.com).

It sends a couple of requests to the Gemini API, and prints the responses
back to the user.

API details:

- [Gemini API](https://ai.google.dev)
- [Python client library](https://github.com/google-gemini/generative-ai-python/blob/main/docs/api/google/generativeai.md)

## How It Works

1. Send an HTTP GET request to trigger the workflow.
2. The workflow prints the responses of Gemini

## Deployment & Configuration

### Cloud Usage

- Initialize your connection with Gemini through the UI

### self-hosted

#### Prerequisites

- [Install AutoKitteh](https://docs.autokitteh.com/get_started/install)

#### Installation Steps

1. Clone the repository:
   ```shell
   git clone https://github.com/autokitteh/kittehub.git
   cd kittehub/samples/google/gemini
   ```

2. Start the AutoKitteh server:
   ```shell
   ak up --mode dev
   ```

3. Deploy the project:
   ```shell
   ak deploy --manifest autokitteh.yaml
   ```

   The output will show your connection IDs, which you'll need for the next step. Look for lines like:
   ```shell
   [exec] create_connection "gemini_sample/gemini_connection": con_01je39d6frfdtshstfg5qpk8sz created
   ```
   
   In this example, `con_01je39d6frfdtshstfg5qpk8sz` is the connection ID.

4. Initialize your connections using the CLI:
   ```shell
   ak connection init gemini_connection <connection ID>
   ```


---
title: Gemini sample
description: Simple usage of the Gemini API
integrations: ["googlegemini"]
categories: ["AI", "Samples"]
---

# Gemini Sample

[![Start with AutoKitteh](https://autokitteh.com/assets/autokitteh-badge.svg)](https://app.autokitteh.cloud/template?name=samples/google/gemini)

This [AutoKitteh](https://github.com/autokitteh/autokitteh) project demonstrates integration with [Gemini](https://gemini.google.com) for generating content and conducting interactive chats.

API documentation:

- [Gemini API](https://ai.google.dev)
- [Python client library](https://github.com/google-gemini/generativeai-python/blob/main/docs/api/google/generativeai.md)

## Cloud Usage

1. Initialize your connection with Gemini
2. Deploy project

## Trigger Workflow

> [!IMPORTANT]
> Ensure that the connection with Gemini is properly initialized; otherwise, the workflow will raise a `ConnectionInitError`.

The workflow is triggered by sending an HTTP GET request.

## Self-Hosted Deployment

Follow [these detailed instructions](https://docs.autokitteh.com/get_started/deployment) to deploy the project on a self-hosted server.

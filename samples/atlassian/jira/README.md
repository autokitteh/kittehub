---
title: Jira sample
description: Samples using Jira APIs
integrations: ["jira"]
categories: ["Samples"]
---

# Atlassian Jira Sample

[![Start with AutoKitteh](https://autokitteh.com/assets/autokitteh-badge.svg)](https://app.autokitteh.cloud/template?name=samples/atlassian/jira)

This [AutoKitteh](https://github.com/autokitteh/autokitteh) project
demonstrates 2-way integration with
[Jira](https://www.atlassian.com/software/jira/guides/).

Jira API documentation:

- [REST API](https://developer.atlassian.com/cloud/jira/platform/rest/v3/intro/)
- ["Atlassian Python API" Python library](https://atlassian-python-api.readthedocs.io/)
- ["Jira" Python library](https://jira.readthedocs.io/)

Python code samples:

- [Atlassian Python API](https://github.com/atlassian-api/atlassian-python-api/tree/master/examples/jira)
- [Jira](https://github.com/pycontribs/jira/tree/main/examples)

This program isn't meant to cover all available functions and events. It
merely showcases a few illustrative, annotated, reusable examples.

## How It Works

1. Adds a comment to a new Jira issue when it is created
2. When a comment is added to an issue, another comment will be added displaying the name of the comments' author

## Cloud Usage

1. Initialize your connection with Jira
2. Deploy project

> [!NOTE]
> For more details on connection options and setup, visit [this guide](https://docs.autokitteh.com/integrations/atlassian/connection).

## Self-Hosted Deployment

Follow [these detailed instructions](https://docs.autokitteh.com/get_started/deployment) to deploy the project on a self-hosted server.

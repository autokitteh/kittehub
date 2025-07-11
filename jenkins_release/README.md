---
title: GitHub and Jenkins workflow
description: This ensures that when a commit is pushed to main, a specific Jenkins build is completed.
integrations: ["github"]
categories: ["DevOps"]
tags: ["webhook_handling", "retry_mechanisms", "monitoring", "notifications"]
---

# GitHub and Jenkins Workflow

[![Start with AutoKitteh](https://autokitteh.com/assets/autokitteh-badge.svg)](https://app.autokitteh.cloud/template?name=jenkins_release)

Some jobs are sometimes required to pass, knowing that all their inputs as valid. In this case we demonstrate that by ensuring that a specific Jenkins job is retries until passing when a new push happens on main.

## How It Works

1. Receive a push to main event from GitHub.
2. Repeatedly create a build on Jenkins and retry it until it's passing.

## Jenkins Job

The desired Jenkins job should receive a single parameter called "sha".

## Self-Hosted Deployment

- Follow these [detailed instructions](https://docs.autokitteh.com/get_started/deployment) to deploy the project on a self-hosted server.

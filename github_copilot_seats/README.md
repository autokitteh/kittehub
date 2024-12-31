---
title: Unregister non active users from Copilot
description: If Copilot was not used in a preceding period by users, the workflow automatically unregisters and notifies them. Users can ask for their subscription to be reinstated.
integrations: ["githubcopilot", "slack"]
categories: ["DevOps"]
---

# GitHub Copilot Registration Pruning

This automation searches daily for all users in a GitHub organization that are actively using Copilot.
If Copilot was not used in a preceding period, it automatically unregisters them, and then notifies them.
Users can then optionally ask for their subscription to be reinstated.

## Before Deploying This AutoKitteh Project:

- Set the `GITHUB_ORG` in the project's vars.
- Set the `IDLE_USAGE_THRESHOLD` in the project's vars:
  - (e.g., `4320` for 72 hours)
  - (e.g., `25` for 25 minutes)
- Set the `LOGINS` in the project's vars (optional).
- Set the `LOG_CHANNEL` in the project's vars to the Slack channel name/ID you want to post to.

## Slack Usage

- `/autokitteh prune-idle-copilot-seats` invokes the automation immediately.
- `/autokitteh find-idle-copilot-seats` displays the potentially idle seats.

> [!WARNING]
> This example currently works only with a [Personal Access Token](https://docs.autokitteh.com/integrations/github/connection/#personal-access-token-pat), specifically a [classic token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-personal-access-token-classic).

---
title: Cancel GitHub Copilot access for inactive users
description: If Copilot was not used in a preceding period by users, unsubscribe and notify them in Slack. Users can ask for their subscription to be reinstated.
integrations: ["githubcopilot", "slack"]
categories: ["DevOps"]
---

# GitHub Copilot Seat Pruning

This automation enumerates once a day all the users in the GitHub organization
that have access to [Copilot](https://github.com/features/copilot). If any of
them haven't used it in a preceding period of time, it automatically marks
their seat for cancellation in the next billing cycle, and notifies them in a
Slack DM.

Users can then optionally respond and ask for the seat to be reassigned back
to them.

## Before Deploying This AutoKitteh Project

Set/modify these optional project variables:

- `IDLE_HOURS_THRESHOLD` (default = 72 hours)
- `MANAGED_LOGINS` (default = no one = manage all org users)
- `SLACK_LOG_CHANNEL` (default = `"copilot-log"`, `""` = no logging in Slack)

## Slack Usage

You may use the Slack application's slash command(s) with one of these text
triggers:

- `prune-idle-copilot-seats` - invokes the daily automation immediately
- `find-idle-copilot-seats` - displays the potentially idle seats

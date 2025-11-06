---
title: Cancel GitHub Copilot access for inactive users
description: If Copilot was not used in a preceding period by users, unsubscribe and notify them in Slack. Users can ask for their subscription to be reinstated.
integrations: ["github", "slack"]
categories: ["DevOps"]
tags:
  [
    "child_sessions",
    "interactive_workflows",
    "user_interactions",
    "start",
    "subscribe",
    "next_event",
    "essential",
  ]
---

# GitHub Copilot Seat Pruning

[![Start with AutoKitteh](https://autokitteh.com/assets/autokitteh-badge.svg)](https://app.autokitteh.cloud/template?template-name=github_copilot_seats)

This automation runs daily to list all the users in the GitHub organization
who have access to [Copilot](https://github.com/features/copilot). If any of
them haven't used it in a preceding period of time, it marks their seat for
cancellation in the next billing cycle, and notifies them in a Slack DM.

Users can then optionally respond and ask for the seat to be reassigned back
to them.

## How It Works

1. Monitor GitHub Copilot seat assignments using a scheduled workflow
2. Identifies idle Copilot seats based on the last activity of assigned users, comparing it to a predefined inactivity threshold (`IDLE_HOURS_THRESHOLD`)
3. If idle seats are found, interacts with users through Slack to confirm seat removal or reinstatement

## Cloud Usage

1. Initialize your connections (GitHub, Slack)
2. Set/modify these optional project variables:
   - `IDLE_HOURS_THRESHOLD` (default = 72 hours)
   - `MANAGED_LOGINS` (default = no one = manage all org users)
   - `SLACK_LOG_CHANNEL` (channel name or ID, default = none)
3. Deploy project

## Trigger Workflow

- Use the Slack application's slash command(s) with one of these text triggers:
  - `prune-idle-copilot-seats` - invokes the daily automation immediately
  - `find-idle-copilot-seats` - displays the potentially idle seats
- `on_schedule` is scheduled to run daily to identify and print idle seats using the `seats.find_idle_seats` function

## Self-Hosted Deployment

Follow [these detailed instructions](https://docs.autokitteh.com/get_started/deployment) to deploy the project on a self-hosted server.

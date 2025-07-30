---
title: Scheduler sample
description: Samples using cron scheduler for workflows
integrations: []
categories: ["Samples"]
tags: ["scheduler"]
---

# Scheduler (Cron) Sample

[![Start with AutoKitteh](https://autokitteh.com/assets/autokitteh-badge.svg)](https://app.autokitteh.cloud/template?name=samples/scheduler)

This project demonstrates
[AutoKitteh](https://github.com/autokitteh/autokitteh)'s
cron-like scheduler.

It scans a specific GitHub repo on a daily basis to identify stalled PRs. If
any are found, it prints a message about them.

## API Documentation

- [Cron expression format](https://pkg.go.dev/github.com/robfig/cron/v3#hdr-CRON_Expression_Format)
  ("\* \* \* \* \*")

- [Cron extended expression format](https://pkg.go.dev/github.com/robfig/cron/v3#hdr-Alternative_Formats)
  (includes seconds and minutes)

- [Predefined schedules and intervals](https://pkg.go.dev/github.com/robfig/cron#hdr-Predefined_schedules)
  ("@" format)

  - `@yearly`/`@annually`, `@monthly`, `@weekly`, `@daily`/`@midnight`, `@hourly`
  - `@every 1h30m10s`

- [Crontab.guru - cron schedule expression editor](https://crontab.guru/)

## How It Works

1. Fetch open pull requests from the specified GitHub repository, excluding drafts and WIP (Work in Progress) PRs
2. Check each PR against predefined thresholds for how long it has been open (`OPENED_CUTOFF`) and when it was last updated (`UPDATE_CUTOFF`)
3. Identify stalled PRs that exceed these thresholds and prints their details

## Cloud Usage

1.  Initialize your connection with GitHub
2.  Update the project variables `GITHUB_OWNER`, `GITHUB_REPO`, `OPENED_CUTOFF`, and `UPDATE_CUTOFF` to configure the repository and thresholds
3.  Deploy project

## Trigger Workflow

The workflow triggers automatically based on the configured cron job, users can customize the scheduling in the `TRIGGERS` section.

## Self-Hosted Deployment

Follow [these detailed instructions](https://docs.autokitteh.com/get_started/deployment) to deploy the project on a self-hosted server.

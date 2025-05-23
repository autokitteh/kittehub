---
title: Fault tolerant workflow with manual Slack approvals
description: Runs a sequence of tasks with fault tolerance. In case of failure, user can decide to terminate or retry from the point of failure.
integrations: ["slack"]
categories: ["Durability"]
---

# Fault Tolerant Workflow with Manual Slack Approvals

[![Start with AutoKitteh](https://autokitteh.com/assets/autokitteh-badge.svg)](https://app.autokitteh.cloud/template?name=task_chain/single_workflow/basic)

This project automates a sequence of tasks with fault tolerance. In case of failure, user can decide to terminate or retry from the point of failure.

## How It Works

1. Trigger workflow execution through a Slack slash command
2. Execute sequential tasks (steps 1-4) with error monitoring
3. Detect task failures and notify user via Slack
4. Process user decisions to retry failed tasks or terminate workflow
5. Complete workflow with success notification to user

## Cloud Usage

1. Initialize your Slack connection
2. Deploy project

## Trigger Workflow

Trigger workflow execution using the Slack slash command:

`/autokitteh <user_id>`

> [!NOTE]
> If you are using a self-hosted deployment, your command may vary depending on your configured command prefix.

## Self-Hosted Deployment

Follow [these detailed instructions](https://docs.autokitteh.com/get_started/deployment) to deploy the project on a self-hosted server.

---
title: OpenAI Agent Researcher
description: A Slack-based research agent workflow.
integrations: ["chatgpt", "slack"]
categories: ["AI"]
tags: ["interactive_workflows", "user_interactions", "activity"]
---

[Blog Post](https://autokitteh.com/technical-blog/building-stateful-ai-research-agent-with-openai-agents/)

# OpenAI Agent Researcher

[![Start with AutoKitteh](https://autokitteh.com/assets/autokitteh-badge.svg)](https://app.autokitteh.cloud/template?name=ai_agents/openai_agent_researcher)

An interactive AI research assistant that uses OpenAI Agents to perform web searches and gather information based on user queries. Built on the durable AutoKitteh platform, this assistant communicates with users through Slack, plans research tasks, and delivers comprehensive reports with fault-tolerant execution.

API documentation:

- openai-agents: https://platform.openai.com/docs/guides/agents

## How It Works

1. In any Slack channel where the bot is present, use the command:

   ```
   !research [your research question]
   ```

2. The assistant will:

   - Generate a research plan
   - Ask for confirmation
   - Execute searches
   - (Optionally) Ask specific people questions
   - Compile a final report

3. The assistant can be instructed to send reports to specific users with the appropriate command.

## Cloud Usage

1. Initialize Slack connection
2. Configure the `OPENAI_API_KEY` project variable with your API key
3. Configure the `INVOCATION_CMD` variable to set the command prefix (default: "research")
4. Deploy project

## Trigger Workflow

> [!IMPORTANT]
> Ensure the Slack connection is initialized; otherwise, the workflow will raise a `ConnectionInitError`.

In any Slack channel where the bot is present, use the command:

```
!research [your research question]
```

## Self-Hosted Deployment

Follow [these detailed instructions](https://docs.autokitteh.com/get_started/deployment) to deploy the project on a self-hosted server.

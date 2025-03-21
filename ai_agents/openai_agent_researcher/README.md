---
title: OpenAI Agent Researcher
description: A Slack-based research agent workflow.
integrations: ["chatgpt", "slack", "openai"]
categories: ["AI"]
---

# OpenAI Agent Researcher

An interactive AI research assistant that uses OpenAI Agents to perform web searches and gather information based on user queries. Built on the durable AutoKitteh platform, this assistant communicates with users through Slack, plans research tasks, and delivers comprehensive reports with fault-tolerant execution.

## Features

- **Interactive Planning**: Generates a research plan based on user queries
- **Web Search Integration**: Searches the web for relevant information
- **Human Collaboration**: Can ask specific people questions as part of the research
- **Report Generation**: Synthesizes research findings into comprehensive reports
- **Slack Integration**: Communicates with users through Slack

## Components

### Core Modules

- **workflow.py**: Main entry point handling the end-to-end research workflow
- **ai.py**: Defines AI agents for planning, searching, and reporting
- **data.py**: Contains data models for the research plan and report
- **slack.py**: Handles Slack communication
- **tools.py**: Defines tools for the OpenAI agents

### Agents

1. **PlannerAgent**: Creates a research plan from user queries
2. **SearchAgent**: Performs web searches and summarizes results
3. **ReporterAgent**: Synthesizes findings into a cohesive report

## Setup

### Prerequisites

- OpenAI API key with access to GPT-4
- Slack workspace with bot permissions
- Access to AutoKitteh Cloud

### Setup

1. In the AutoKitteh Cloud UI:
   - Configure the `OPENAI_API_KEY` project variable with your API key
   - Configure the `INVOCATION_CMD` variable to set the command prefix (default: "research")
2. Initialize the Slack connection through the AutoKitteh Cloud UI
3. Deploy the project using AutoKitteh Cloud

## Usage

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

## Workflow

1. **Planning Phase**: The PlannerAgent creates a research plan with 3-10 tasks
2. **Execution Phase**: Tasks are executed (searches, questions to individuals)
3. **Reporting Phase**: Results are synthesized into a report

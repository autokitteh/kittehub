---
title: LangGraph Bot with Tavily, and Google Sheets
description: Slack bot built with LangGraph and powered by Gemini LLM that can search information and update Google Sheets
integrations: ["slack", "googlesheets"]
categories: ["AI", "Productivity"]
tags: ["user_interactions", "notifications", "webhook_handling", "data_processing"]
---

# LangGraph Bot with Tavily, and Google Sheets

[![Start with AutoKitteh](https://autokitteh.com/assets/autokitteh-badge.svg)](https://app.autokitteh.cloud/template?template-name=ai_agents/langgraph_bot)

This [AutoKitteh](https://github.com/autokitteh/autokitteh) project integrates Slack messaging with the power of [Google Gemini LLM](https://cloud.google.com/vertex-ai/docs/generative-ai/learn/models), [Tavily Search API](https://tavily.com), and [LangGraph](https://github.com/langchain-ai/langgraph), enabling a bot that can answer user queries and update Google Sheets dynamically.

## API Documentation

- Slack: https://docs.autokitteh.com/integrations/slack
- Google Sheets: https://docs.autokitteh.com/integrations/google/sheets
- Tavily Search: https://docs.tavily.com/

## How It Works

1. Mention the slack app in a message and provide your prompt
2. The LangGraph-based workflow decides:
   - Use Tavily to search for external information if needed
   - Or call Google Sheets API to update data
3. The bot responds in Slack with either search results or a success message after writing to the Sheet

The bot can:

- Answer user queries via web search (Tavily)
- Insert user-specified tables into a Google Sheet
- Respond conversationally based on Gemini LLM

## Cloud Usage

1. Initialize your connections:

   - Slack connection (`slack_conn`)
   - Google Sheets connection (`sheets_conn`)

2. Set the required environment variables:

   - `GOOGLE_API_KEY`
   - `TAVILY_API_KEY`

3. Deploy project

## Trigger Workflow

Mention the Slack app and include the prompt in the message.

Example prompts:

- `@YourAppName What's the tallest mountain in the world?`
- `@YourAppName Write to sheet 'SHEET_ID' this table: date,name\n1,one\n2,two\n3,three`

> [!TIP]
> When writing tables, use a simple CSV-style format where each row is separated by a newline (`\n`).

## Self-Hosted Deployment

Follow [these detailed instructions](https://docs.autokitteh.com/get_started/deployment) to deploy the project on a self-hosted server.

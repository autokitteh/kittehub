---
title: AI chat assistant
description: A Slack-based automation assistant that leverages ChatGPT to manage and respond to messages by integrating with GitHub and Google Sheets.
integrations: ["chatgpt", "github", "sheets", "slack"]
categories: ["AI"]
---

# AI Chat Assistant

[![Start with AutoKitteh](https://autokitteh.com/assets/autokitteh-badge.svg)](https://app.autokitteh.cloud/template?name=ai-chat-assistant)

This project automates the process of managing and responding to messages through Slack. By integrating with ChatGPT, GitHub, Google Sheets, and Slack, it can interpret plain-English commands into structured actions. The assistant can perform key functions like listing tasks stored in Google Sheets or scanning GitHub repositories for unanswered comments, making it easier to keep track of open issues and follow-ups.

API Documentation:

- [OpenAI ChatGPT API](https://openai.com/)
- [GitHub API](https://docs.github.com/en/rest)
- [Google Sheets API](https://developers.google.com/sheets)
- [Slack API](https://api.slack.com/)

## How It Works

1. Listen for incoming messages in Slack
2. Send incoming commands to ChatGPT to determine action (either "list" or "scan")
3. Execute determined action:
   - For list action: Retrieve stored unanswered comments from Google Sheet
   - For scan action: Search GitHub repository for unanswered comments and store them in the same Google Sheet
4. Format results and send back through Slack message

## Cloud Usage

1. Initialize your connections (ChatGPT, GitHub, Google Sheets, and Slack)
2. Configure the `REPO_NAME`, `SHEET_ID`, and `SHEET_NAME` project variables
3. Deploy the project
4. Start the AI Chat Assistant by manually running the `on_activate` function in `ai.py`

## Trigger Workflow

> [!IMPORTANT]
> Ensure all connections (ChatGPT, GitHub, Google Sheets, and Slack) are properly initialized; otherwise, the workflow will raise a `ConnectionInitError`.

Send a direct message to the bot in Slack to trigger the workflow. The message can be a natural language request like "list my tasks" or "scan for new comments".

## Self-Hosted Deployment

For self-hosted deployment, follow [Autokitteh's deployment instructions](https://docs.autokitteh.com/get_started/deployment) to configure and run the project on your server.

## Known Limitations

- Limited to **list** and **scan** actions
- **scan** must be triggered manually via message
- ChatGPT has no message history

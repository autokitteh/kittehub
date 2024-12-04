---
title: Hackernews Alert with Slack 
description: A bot that tracks Hacker News articles by topic and sends updates to Slack.
integrations: ["slack"]
categories: ["Office Automation"]
---

# Hacker News Alerts in Slack

This project monitors Hacker News for new articles matching a specific topic, fetching their details in real-time. It compares the latest results with previously fetched articles to identify new ones and sends their title and URL as notifications to a Slack channel.

## How It Works

1. Reads the topic from the Slack command.
2. Adds the topic to the search query of HackerNews. Check out https://www.algolia.com/doc/api-reference/rest-api for more details. 
3. Returns the new articles related to the topic that are published after the code started.


## Deployment & Configuration

### Cloud Usage (Recommended)

- Initialize your connection with slack through the UI


## Trigger Workflow

- Type `/your_slack_app` `topic` in the Slack channel you set in the environment variable, replacing `topic` with what you want to search for, to start tracking articles.
- The workflow runs automatically every two minutes after deployment. 

#### Prerequisites
- [Install AutoKitteh](https://docs.autokitteh.com/get_started/install)
- Set up required integrations:
  - [Slack](https://docs.autokitteh.com/integrations/slack)

#### Installation Steps
1. Clone the repository:
   ```shell
   git clone https://github.com/autokitteh/kittehub.git
   cd kittehub/hackernews
   ```

2. Start the AutoKitteh server:
   ```shell
   ak up --mode dev
   ```

3. Deploy the project:
   ```shell
   ak deploy --manifest autokitteh.yaml
   ```

   The output will show your connection IDs, which you'll need for the next step. Look for lines like:
   ```shell
   [exec] create_connection "hackernews_alert/slack_connection": con_01je39d6frfdtshstfg5qpk8sz created
   ```
   
   In this example, `con_01je39d6frfdtshstfg5qpk8sz` is the connection ID.

4. Initialize your connections using the CLI:
   ```shell
   ak connection init slack_connection <connection ID>
   ```


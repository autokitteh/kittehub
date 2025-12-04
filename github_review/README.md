---
title: GitHub Review - PR Review Request Bot
description: Slash command bot for requesting and removing PR reviews via comments
integrations: ["github"]
categories: ["Productivity", "DevOps"]
tags: ["github", "pull_requests", "code_review", "slash_commands"]
---

# GitHub Review - PR Review Request Bot

[![Start with AutoKitteh](https://autokitteh.com/assets/autokitteh-badge.svg)](https://app.autokitteh.cloud/template?name=github_review)

A GitHub bot that lets team members request and remove PR reviews using slash commands in PR comments. Simplify the review process by typing `/review` or `/unreview` to manage review requests directly from comments.

## Features

- **Slash Command Interface**: Use `/review` and `/unreview` commands in PR comments
- **Multiple Reviewers**: Request reviews from multiple users in a single command
- **Self Removal**: Type `/unreview` with no arguments to remove yourself as a reviewer
- **Permission Checking**: Only collaborators can request reviews
- **Emoji Reactions**: Visual feedback with emoji reactions on commands
- **Automated Responses**: Bot replies with confirmation or error messages

## Why?

Managing PR reviews often requires navigating GitHub's UI or having specific permissions. This automation allows collaborators to request and manage reviews directly through PR comments, making the review process more accessible and streamlined.

### What [AutoKitteh](https://autokitteh.com) Provides

- Event-driven GitHub integration
- No server configuration needed
- Built-in GitHub API client
- Automatic event filtering
- Production ready deployment

## How It Works

1. **Comment on a PR** with `/review` or `/unreview`
2. **Bot Processes Command**: Validates permissions and reviewers
3. **Updates PR**: Adds or removes review requests
4. **Provides Feedback**: Adds emoji reaction and confirmation comment

## Usage

### Request Reviews

**Request review from specific users:**

```
/review @username
```

**Request reviews from multiple users:**

```
/review @user1 @user2 @user3
```

### Remove Review Requests

**Remove yourself as a reviewer:**

```
/unreview
```

**Remove specific users from reviewers:**

```
/unreview @username
```

**Remove multiple users from reviewers:**

```
/unreview @user1 @user2
```

## Deployment

Deploy using the AutoKitteh CLI or web interface:

[![Start with AutoKitteh](https://autokitteh.com/assets/autokitteh-badge.svg)](https://app.autokitteh.cloud/template?name=github_review)

### Command Line Deployment

1. **Install the CLI**: https://docs.autokitteh.com/get_started/install
2. **Authenticate**: `ak auth login`
3. **Deploy**: `make deploy`
4. **Initialize connection**: Log in to https://autokitteh.cloud and initialize the GitHub connection
5. **Configure repository**: Set up the connection to watch your GitHub repository

## Connections

- **github** (required): GitHub integration for receiving PR comment events and managing review requests

## Implementation Details

### Core Files

- **`handlers.py`** (`handlers.py:10`): Main event handlers
  - `on_review_issue_comment()`: Processes `/review` commands
  - `on_unreview_issue_comment()`: Processes `/unreview` commands
  - `_respond()`: Sends confirmation messages and emoji reactions

### How It Uses AutoKitteh

The system uses AutoKitteh's event-driven architecture:

```python
from autokitteh import Event
from autokitteh.github import github_client
```

1. **Event Triggers** (`autokitteh.yaml:11`): GitHub issue comment events

   ```yaml
   triggers:
     - name: review_issue_comment
       connection: github
       event_type: issue_comment
       call: handlers.py:on_review_issue_comment
       filter: "data.comment.body.startsWith('/review') && (data.action in ['created', 'opened'])"
   ```

2. **Event Filtering**: Only processes comments starting with `/review` or `/unreview`

3. **GitHub API Integration** (`handlers.py:57`): Built-in GitHub client
   ```python
   github = github_client("github")
   repo = github.get_repo(data["repository"]["full_name"])
   pr = repo.get_pull(number=n)
   pr.create_review_request(reviewers=reviewers)
   ```

### Permission Checks

The bot verifies that:

- The command issuer is a repository collaborator
- All specified reviewers are valid collaborators
- Users have appropriate permissions before making changes

### Bot Responses

The bot provides feedback through:

- **Emoji reactions**: `+1` for success, `confused` for errors
- **Comment replies**: Confirmation messages with details about who was added/removed as reviewers

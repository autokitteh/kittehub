---
title: GitHub Assign - Issue Assignment Bot
description: Slash command bot for assigning and unassigning GitHub issues via comments
integrations: ["github"]
categories: ["Productivity", "DevOps"]
tags: ["github", "issue_management", "slash_commands"]
---

# GitHub Assign - Issue Assignment Bot

[![Start with AutoKitteh](https://autokitteh.com/assets/autokitteh-badge.svg)](https://app.autokitteh.cloud/template?name=github_assign)

A simple GitHub bot that lets team members assign and unassign issues using slash commands in issue comments. No need for special permissions or manual navigation - just type `/assign` or `/unassign` to manage issue assignments directly from comments.

## Features

- **Slash Command Interface**: Use `/assign` and `/unassign` commands in issue comments
- **Self Assignment**: Type `/assign` with no arguments to assign yourself
- **Multiple Assignees**: Assign multiple users in a single command
- **Permission Checking**: Only authorized team members can assign issues
- **Emoji Reactions**: Visual feedback with emoji reactions on commands
- **Automated Responses**: Bot replies with confirmation or error messages

## Why?

Some OSS projects want to allow people assign issues and PRs to valid assignees without giving them the permission to do so in GitHub. This automation allows people to assign valid assignees via issue/pr comments.

### What [AutoKitteh](https://autokitteh.com) Provides

- Event-driven GitHub integration
- No server configuration needed
- Built-in GitHub API client
- Automatic event filtering
- Production ready deployment

## How It Works

1. **Comment on an Issue** with `/assign` or `/unassign`
2. **Bot Processes Command**: Validates permissions and assignees
3. **Updates Issue**: Adds or removes assignees
4. **Provides Feedback**: Adds emoji reaction and confirmation comment

## Usage

### Assign Issues

**Assign yourself:**

```
/assign
```

**Assign specific users:**

```
/assign @username
```

**Assign multiple users:**

```
/assign @user1 @user2 @user3
```

### Unassign Issues

**Unassign yourself:**

```
/unassign
```

**Unassign specific users:**

```
/unassign @username
```

**Unassign multiple users:**

```
/unassign @user1 @user2
```

## Deployment

Deploy using the AutoKitteh CLI or web interface:

[![Start with AutoKitteh](https://autokitteh.com/assets/autokitteh-badge.svg)](https://app.autokitteh.cloud/template?name=github_assign)

### Command Line Deployment

1. **Install the CLI**: https://docs.autokitteh.com/get_started/install
2. **Authenticate**: `ak auth login`
3. **Deploy**: `make deploy`
4. **Initialize connection**: Log in to https://autokitteh.cloud and initialize the GitHub connection
5. **Configure repository**: Set up the connection to watch your GitHub repository

## Connections

- **github** (required): GitHub integration for receiving issue comment events and managing assignments

## Implementation Details

### Core Files

- **`handlers.py`** (`handlers.py:10`): Main event handlers
  - `on_assign_issue_comment()`: Processes `/assign` commands
  - `on_unassign_issue_comment()`: Processes `/unassign` commands
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
     - name: assign_issue_comment
       connection: github
       event_type: issue_comment
       call: handlers.py:on_assign_issue_comment
       filter: "data.comment.body.startsWith('/assign') && (data.action in ['created', 'opened'])"
   ```

2. **Event Filtering**: Only processes comments starting with `/assign` or `/unassign`

3. **GitHub API Integration** (`handlers.py:7`): Built-in GitHub client
   ```python
   github = github_client("github")
   repo = github.get_repo(data["repository"]["full_name"])
   issue = repo.get_issue(number=data["issue"]["number"])
   ```

### Permission Checks

The bot verifies that:

- The command issuer is in the repository's assignees list
- All specified assignees are valid for the repository
- Users have appropriate permissions before making changes

### Bot Responses

The bot provides feedback through:

- **Emoji reactions**: `+1` for success, `confused` for errors
- **Comment replies**: Confirmation messages with details about who was assigned/unassigned

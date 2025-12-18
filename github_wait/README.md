---
title: GitHub Wait - PR/Issue State Management Bot
description: Slash command bot for managing waiting states on PRs and issues with automatic label updates
integrations: ["github"]
categories: ["Productivity", "DevOps"]
tags: ["github", "pull_requests", "issue_management", "slash_commands", "labels"]
---

# GitHub Wait - PR/Issue State Management Bot

[![Start with AutoKitteh](https://autokitteh.com/assets/autokitteh-badge.svg)](https://app.autokitteh.cloud/template?name=github_wait)

A GitHub bot that helps reviewers track PRs that are waiting for author updates. Reviewers can mark PRs with `/wait` after completing their review, and the bot automatically removes the label when the author pushes new changes - making it easy to see at a glance which PRs are ready for re-review.

## Features

- **Quick PR Triage**: Reviewers can instantly see which PRs have been updated and need attention
- **Automatic Label Removal**: Labels disappear when authors push new code - no manual cleanup needed
- **Slash Command Interface**: Simple `/wait` or `/wait-any` commands in review comments
- **Two Wait Modes**:
  - `/wait` - removed only when author pushes code (ideal for "changes requested")
  - `/wait-any` - removed when author comments or pushes code (for discussions)
- **Visual Feedback**: Emoji reactions confirm command execution
- **Works Everywhere**: Use in PR reviews, review comments, or regular comments

## Why?

Active reviewers often manage dozens of PRs simultaneously. The problem: **when looking at a PR list, it's hard to tell which PRs have been updated since your last review.**

GitHub's native notifications don't give you an at-a-glance view of what needs attention. This bot solves that by:

- **After reviewing**: Mark the PR with `/wait` to indicate you're waiting for the author
- **Author updates**: When they push new code, the label automatically disappears
- **Quick scanning**: Filter your PR list by the waiting label to see what needs re-review
- **No manual cleanup**: Labels remove themselves - no stale markers cluttering your views

For reviewers handling many PRs, this creates a self-maintaining "reviewed, waiting for author" queue that updates automatically as authors respond.

### What [AutoKitteh](https://autokitteh.com) Provides

- Event-driven GitHub integration
- No server configuration needed
- Built-in GitHub API client
- Automatic event filtering
- Production ready deployment

## How It Works

### Typical Reviewer Workflow

1. **Review a PR**: Complete your code review and request changes
2. **Mark as waiting**: Add `/wait` in your review comment
3. **Bot adds label**: The `waiting` label appears on the PR
4. **Author pushes code**: When they address your feedback and push commits
5. **Label auto-removes**: The bot detects the push and removes the label
6. **You see it's ready**: The PR disappears from your "waiting" filter - time to review again!

### Wait Modes

**`/wait` (waiting for code changes)** - Best for most reviews
- Adds `waiting` label
- Label removed only when author pushes new code
- Ideal after requesting changes or when specifically waiting for code updates

**`/wait-any` (waiting for any response)** - For discussions
- Adds `waiting:any` label
- Label removed when author comments OR pushes code
- Use when you need clarification or are waiting for discussion to continue

## Usage

### After Completing a Review

When you finish reviewing a PR and are waiting for the author to make changes:

```
/wait
```

This adds the `waiting` label to the PR. When the author pushes new code, the label automatically disappears.

**Pro tip**: Filter your PR list by `label:waiting` to see all PRs you've reviewed that are still waiting for author updates. When the label disappears, you know it's time to re-review!

### For Discussion-Based Reviews

When you're waiting for the author to respond to questions or clarify something:

```
/wait-any
```

This adds the `waiting:any` label. It will be removed when the author either comments or pushes code.

### Switching Wait Modes

You can change your mind by using the other command - the bot automatically switches labels:

```
/wait       # Adds "waiting" label
/wait-any   # Switches to "waiting:any" label
```

## Deployment

Deploy using the AutoKitteh CLI or web interface:

[![Start with AutoKitteh](https://autokitteh.com/assets/autokitteh-badge.svg)](https://app.autokitteh.cloud/template?name=github_wait)

### Command Line Deployment

1. **Install the CLI**: https://docs.autokitteh.com/get_started/install
2. **Authenticate**: `ak auth login`
3. **Deploy**: `make deploy`
4. **Initialize connection**: Log in to https://autokitteh.cloud and initialize the GitHub connection
5. **Configure repository**: Set up the connection to watch your GitHub repository

## Connections

- **github** (required): GitHub integration for receiving events and managing labels

## Implementation Details

### Core Files

- **`handlers.py`** (`handlers.py:23`): Main event handlers
  - `on_command()`: Processes `/wait` and `/wait-any` commands
  - `on_pull_request_sync()`: Removes waiting labels when new code is pushed
  - `on_issue_comment()`: Removes `waiting:any` label on new issue comments
  - `on_pull_request_review_comment()`: Removes `waiting:any` label on new PR review comments
  - `on_pull_request_review()`: Removes `waiting:any` label on new PR reviews
  - `_label()`: Helper function for adding and removing labels

### How It Uses AutoKitteh

The system uses AutoKitteh's event-driven architecture:

```python
from autokitteh import Event
from autokitteh.github import github_client
```

1. **Event Triggers** (`autokitteh.yaml:10`): Multiple GitHub event types

   ```yaml
   triggers:
     - name: command
       connection: github
       event_type: slash_command
       call: handlers.py:on_command
       filter: "data.command.name in ['wait', 'wait-any'] && (data.actual_event_type in ['issue_comment', 'pull_request_review_comment', 'pull_request_review'])"
   ```

2. **Event Filtering**: Smart filtering based on event types and slash commands

3. **GitHub API Integration** (`handlers.py:10`): Built-in GitHub client
   ```python
   github = github_client("github")
   repo = github.get_repo(data.repository.full_name)
   issue = repo.get_issue(number=data.issue.number)
   issue.add_to_labels("waiting")
   ```

### Labels Used

The bot uses two labels:

- **`waiting`**: Indicates waiting for code changes (push events only)
- **`waiting:any`**: Indicates waiting for any activity (comments or code changes)

These labels should be created in your repository. The bot will create them automatically on first use if they don't exist.

### Smart Activity Detection

The bot intelligently handles different scenarios to prevent false positives:

- **Reviewer Comments**: When reviewers add more comments (including wait commands), labels stay in place
- **Author Comments**: Comments from the author remove the `waiting:any` label (but not `waiting`)
- **Code Pushes**: New commits from the author remove both `waiting` and `waiting:any` labels
- **Reviews**: New review submissions remove the `waiting:any` label

This means reviewers can continue discussing without accidentally removing the waiting state - only author activity triggers label removal.

### Bot Responses

The bot provides feedback through:

- **Emoji reactions**: `+1` emoji on command comments to confirm execution
- **Automatic label management**: Labels appear and disappear based on activity

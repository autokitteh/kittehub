---
title: Reddit sample
description: Simple usage of the Reddit API
integrations: ["reddit"]
categories: ["Samples"]
---

# Reddit Sample

[![Start with AutoKitteh](https://autokitteh.com/assets/autokitteh-badge.svg)](https://app.autokitteh.cloud/template?template-name=samples/reddit)

The Reddit sample demonstrates how to interact with Reddit using AutoKitteh's Reddit integration.

The sample includes two separate workflows:

1. **Create Post** - Create a reddit post
2. **Add a comment** - Add a comment on a reddit post

API details:

- [Reddit API](https://www.reddit.com/dev/api/)
- [PRAW (Python Reddit API Wrapper)](https://praw.readthedocs.io/)

## How It Works

- Create a new post in a specified subreddit
- Add a comment to an existing post by using the post id from the webhook

## Cloud Usage

1. Initialize your Reddit connection through the UI
2. Copy the webhook trigger's URL (for the [Trigger Workflows](#trigger-workflows) section below):
   - Hover over the trigger's (i) icon for the webhook you want to use
   - Click the copy icon next to the webhook URL for your selected trigger
   - (Detailed instructions [here](https://docs.autokitteh.com/get_started/deployment#webhook-urls))
3. Update the `SUBREDDIT` project variable with your target subreddit name (without the "r/" prefix)

## Trigger Workflows

### Create a Post

```shell
curl -X POST "${WEBHOOK_URL}" \
  -d "title=Hello from AutoKitteh" \
  -d "content=This is a test post created with AutoKitteh" \
  -d "flair=<FLAIR_ID>"
```

- Replace `WEBHOOK_URL` with the URL of `create_post_webhook` webhook in the triggers section.
- provide a flair ID, a title and content.

### Add a Comment

```shell
curl -X POST "${WEBHOOK_URL}" \
  -d "post_id=<POST_ID>" \
  -d "comment=Great post!"
```

- Replace `WEBHOOK_URL` with the URL of `add_comment_webhook` webhook in the triggers section.
- Replace `<POST_ID>` with the ID of the Reddit post you want to comment on, and provide the comment.

## Self-Hosted Deployment

Follow these [detailed instructions](https://docs.autokitteh.com/get_started/deployment) to deploy the project on a self-hosted server.

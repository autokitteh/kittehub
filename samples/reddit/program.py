"""Demonstrates AutoKitteh's Reddit integration for managing posts and comments.

This sample shows how to create posts on Reddit, add comments, and retrieve post info.

This program isn't meant to cover all available functions and events.
It merely showcases various illustrative, annotated, reusable examples.
"""

import os

from autokitteh.reddit import reddit_client
from praw.exceptions import RedditAPIException


reddit = reddit_client("reddit_conn")

SUBREDDIT = os.getenv("SUBREDDIT", "")


def create_post(event):
    """Create a new post in a subreddit."""
    if not SUBREDDIT:
        print("Error: SUBREDDIT environment variable is not set")
        return

    form = event.data.body.form
    post_title = form.get("title", "AutoKitteh Post")
    post_content = form.get("content", "Created by AutoKitteh")
    post_flair = form.get("flair", "default")

    try:
        subreddit = reddit.subreddit(SUBREDDIT)
        submission = subreddit.submit(
            post_title, selftext=post_content, flair_id=post_flair
        )
        print(f"Post '{post_title}' created successfully!")
        print(f"Post ID: {submission.id}")
        print(f"Post URL: {submission.url}")
        print(f"Permalink: https://reddit.com{submission.permalink}")
    except RedditAPIException as e:
        print("Failed to create post.")
        print("Error:", str(e))


def add_comment(event):
    """Add a comment to an existing post.

    This function adds a comment to a post using the post ID from form data.

    Args:
        event: The HTTP event containing request data.
    """
    form = event.data.body.form
    post_id = form.get("post_id")
    comment_text = form.get("comment", "Comment from AutoKitteh")

    if not post_id:
        print("Error: post_id parameter is required")
        return

    try:
        submission = reddit.submission(id=post_id)
        comment = submission.reply(comment_text)

        print(f"Comment added successfully to post {post_id}")
        print(f"Comment ID: {comment.id}")
        print(f"Comment URL: https://reddit.com{comment.permalink}")
    except RedditAPIException as e:
        print("Failed to add comment.")
        print("Error:", str(e))

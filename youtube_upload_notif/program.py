"""Poll for new YouTube videos from a specific channel and send to slack."""

from datetime import datetime, UTC
import os

import autokitteh
from autokitteh.google import youtube_client
from autokitteh.slack import slack_client


youtube = youtube_client("youtube_conn")
slack = slack_client("slack_conn")


YT_CHANNEL_NAME = os.getenv("YOUTUBE_CHANNEL_NAME")
SLACK_CHANNEL = os.getenv("SLACK_CHANNEL")
MAX_RESULTS = 5  # Number of videos to check.


def poll_for_new_videos(event):
    """Poll for new videos from the configured YouTube channel.

    This function is triggered by a scheduled cron job.
    It checks for new videos and send to slack info about any new ones found.
    """
    channel_id = get_channel_id()
    if channel_id is None:
        print("no channel found")
        return

    search_response = (
        youtube.search()
        .list(
            part="snippet",
            channelId=channel_id,
            order="date",
            type="video",
            maxResults=MAX_RESULTS,
        )
        .execute()
    )

    videos = search_response.get("items", [])

    if not videos:
        print("No videos found for this channel")
        return

    # Get the last checked timestamp.
    last_checked = autokitteh.get_value("last_checked_timestamp")

    if last_checked:
        last_checked_dt = datetime.fromisoformat(last_checked)
    else:
        current_time = datetime.now(UTC).isoformat()
        autokitteh.set_value("last_checked_timestamp", current_time)
        print("Will be notified about new videos.")
        return

    new_videos = []
    latest_timestamp = last_checked

    for video in videos:
        video_published = video["snippet"]["publishedAt"]
        video_published_dt = datetime.fromisoformat(
            video_published.replace("Z", "+00:00")
        )

        if video_published_dt > last_checked_dt:
            new_videos.append(video)

            if video_published > latest_timestamp:
                latest_timestamp = video_published

    if new_videos:
        for video in new_videos:
            snippet = video["snippet"]
            video_id = video["id"]["videoId"]
            video_url = f"https://www.youtube.com/watch?v={video_id}"

            message = create_slack_message(snippet, video_url)

            slack.chat_postMessage(
                channel=SLACK_CHANNEL,
                text=f"🆕 New video from {YT_CHANNEL_NAME}!",
                blocks=message,
            )

        autokitteh.set_value("last_checked_timestamp", latest_timestamp)


def get_channel_id():
    resp = (
        youtube.search()
        .list(part="snippet", q=YT_CHANNEL_NAME, type="channel", maxResults=1)
        .execute()
    )

    items = resp.get("items") or []
    return items[0]["snippet"]["channelId"] if items else None


def create_slack_message(snippet, video_url):
    """Create a formatted Slack message block for a new video."""
    title = snippet["title"]
    description = snippet["description"]
    published_at = snippet["publishedAt"]
    thumbnail_url = snippet.get("thumbnails", {}).get("medium", {}).get("url", "")

    short_desc = description[:300] + "..." if len(description) > 300 else description

    blocks = [
        {
            "type": "header",
            "text": {"type": "plain_text", "text": "🎬 New YouTube Video!"},
        },
        {
            "type": "section",
            "fields": [
                {"type": "mrkdwn", "text": f"*📺 Channel:*\n{YT_CHANNEL_NAME}"},
                {"type": "mrkdwn", "text": f"*📅 Published:*\n{published_at}"},
            ],
        },
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": f"*{title}*\n\n{short_desc}"},
            "accessory": {
                "type": "button",
                "text": {"type": "plain_text", "text": "▶️ Watch Video"},
                "url": video_url,
                "action_id": "watch_video",
            },
        },
    ]

    if thumbnail_url:
        blocks.append(
            {
                "type": "image",
                "image_url": thumbnail_url,
                "alt_text": f"Thumbnail for {title}",
            }
        )

    return blocks

"""Mirror messages between Slack and Discord channels using.

Discord documentation:
- https://discordpy.readthedocs.io/

Note:
The `discord` import is crucial for enabling specific Discord API
configurations, such as intents and error handling, but all functional
API calls are made through the autokitteh `ak_discord` wrapper, which
streamlines authentication and secret management.
"""

import os

from autokitteh import discord as ak_discord
from autokitteh import slack
import discord


DISCORD_CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID", ""))
SLACK_CHANNEL = os.getenv("SLACK_CHANNEL_NAME_OR_ID", "")

# Discord intents that enable the bot to read message content
intents = discord.Intents.default()
intents.message_content = True

client = ak_discord.discord_client("discord_conn", intents)
slack_api = slack.slack_client("slack_conn")

# Stores the latest message received from Slack, to be posted to Discord
slack_message = None


def on_discord_message(event):
    slack_api.chat_postMessage(channel=SLACK_CHANNEL, text=event.data["content"])


def on_slack_message(event):
    global slack_message
    slack_message = event.data["text"]
    client.run(ak_discord.bot_token("discord_conn"))


@client.event
async def on_ready():
    """An asynchronous event triggered when the Discord bot successfully connects.

    It fetches the Discord channel by ID and sends the latest message received
    from Slack to the channel, then closes the client connection.
    """
    try:
        channel = await client.fetch_channel(DISCORD_CHANNEL_ID)
    except discord.DiscordException as e:
        print(f"Could not find Discord channel with ID: {DISCORD_CHANNEL_ID}: {e}")
        return

    await channel.send(slack_message)

    await client.close()

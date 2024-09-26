"""
This script mirrors messages between Slack and Discord channels using
AutoKitteh's Slack and Discord clients.

Imports:
- `autokitteh.discord as ak_discord`: Wrapper around the Discord API
  client to simplify authentication and secret management.
- `slack`: Module from autokitteh that helps interact with the Slack API.
- `discord`: Necessary import for certain configurations, such as
  enabling message intents, and handling exceptions as outlined in the
  official Discord.py quickstart documentation
  (https://discordpy.readthedocs.io/en/stable/quickstart.html?highlight=
  send%20message#quickstart).

Global Variables:
- `intents`: Discord intents used to enable the bot to read message
  content.
- `client`: The autokitteh Discord client initialized with the necessary
  intents and connection settings.
- `slack_api`: The autokitteh Slack client used to post messages to Slack.
- `slack_message`: Stores the latest message received from Slack to be
  posted to Discord.

- `on_ready()`: An asynchronous event triggered when the Discord bot
  successfully connects. It fetches the Discord channel by ID and sends
  the latest message received from Slack to the channel, then closes the
  client connection.

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


DISCORD_CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))
SLACK_CHANNEL_ID = os.getenv("SLACK_CHANNEL_ID")

intents = discord.Intents.default()
intents.message_content = True
client = ak_discord.discord_client("discord_conn", intents)

slack_api = slack.slack_client("slack_conn")
slack_message = None


def on_discord_message(event):
    slack_api.chat_postMessage(channel=SLACK_CHANNEL_ID, text=event.data["content"])


def on_slack_message(event):
    global slack_message
    slack_message = event.data["text"]
    client.run(ak_discord.bot_token("discord_conn"))


@client.event
async def on_ready():
    try:
        channel = await client.fetch_channel(DISCORD_CHANNEL_ID)
    except discord.DiscordException as e:
        print(f"Could not find Discord channel with ID: {DISCORD_CHANNEL_ID}: {e}")
        return

    await channel.send(slack_message)

    await client.close()

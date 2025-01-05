"""Discprd bot that performs basic operations."""

import os

import autokitteh
import autokitteh.discord as ak_discord
import discord


intents = discord.Intents.default()
intents.message_content = True

client = ak_discord.discord_client("discord_conn", intents)


@autokitteh.activity
def start_event_loop(event):
    """Starts the bot and connects it to the Discord gateway."""
    client.run(ak_discord.bot_token("discord_conn"))


@client.event
async def on_ready():
    """Asynchronous function triggered when the bot successfully connects to Discord."""
    print(f"We have logged in as {client.user}")
    channel_id = int(os.getenv("CHANNEL_ID"))
    channel = client.get_channel(channel_id)

    if channel is None:
        print(f"Channel with ID {channel_id} not found")
        print("Available channels:")
        for guild in client.guilds:
            for channel in guild.channels:
                print(f"{channel.name} (ID: {channel.id})")
        return

    try:
        await channel.send("Meow!")
    except discord.Forbidden:
        print("The bot does not have permission to send messages in this channel.")
    except discord.HTTPException as e:
        print(f"Failed to send message: {e}")
    finally:
        # Closing the client to prevent duplicate messages
        # or unexpected behavior in future workflows.
        await client.close()

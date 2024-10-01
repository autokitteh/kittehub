"""
This program demonstrates how to use Autokitteh's Discord integration to create a bot that performs basic operations.

Modules:
    - autokitteh.discord: Custom wrapper for the Discord API client.
    - discord: The native Discord client API.

Functions:
    - on_ready: An asynchronous function that is triggered when the bot successfully connects to Discord.
        It checks for the availability of a specified channel and sends a message if the channel is found.
        Handles permission and HTTP-related exceptions when attempting to send the message.

    - on_http_get: An AutoKitteh activity that runs the bot when an HTTP GET request is received.
        Retrieves the bot token and initiates the bot connection.

    - client.run(token): Starts the bot and connects it to the Discord gateway.
        This function blocks execution until the bot is stopped. While running, the bot listens for and
        responds to events, such as `on_ready`.

        The `run` method initializes the event loop for the bot, connecting it to Discord using the specified token.
        Once the connection is established, it triggers the `on_ready` event, allowing the bot to perform any
        startup actions, such as checking for available channels and sending messages. This combination of
        `run` and `on_ready` forms the backbone of the bot's lifecycle:
            - `run` starts the bot and maintains the connection to Discord.
            - `on_ready` is triggered automatically when the connection to Discord is fully established.

Notes:
    - This bot listens for the `on_ready` event to confirm a successful connection.
    - The bot sends a "Meow!" message to the specified channel once connected.
"""

import os

import autokitteh
import autokitteh.discord as ak_discord
import discord


intents = discord.Intents.default()
intents.message_content = True

client = ak_discord.discord_client("discord_conn", intents)


@autokitteh.activity
def start_event_loop(event):
    client.run(ak_discord.bot_token("discord_conn"))
    return


@client.event
async def on_ready():
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
        # Closing the client to prevent duplicate messages or unexpected behavior in future workflows
        await client.close()

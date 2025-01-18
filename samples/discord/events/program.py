"""Handle message-related events in Discord.

Also log the corresponding information using the `autokitteh.discord` client.
"""


def on_discord_message_create(event):
    print(f"User {event.data['author']['username']} sent: {event.data['content']}")


def on_discord_message_update(event):
    print(f"Message updated to: {event.data['content']}")


def on_discord_message_delete(event):
    print(f"Message with ID {event.data['id']} was deleted")

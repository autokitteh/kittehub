"""Simple Slack bot using AutoKitteh.

This bot listens to Slack messages and responds to basic commands.
"""

# AutoKitteh SDK - provides easy access to integrations.
# Import the specific client you need from autokitteh.{service}.
from autokitteh.slack import slack_client


# Initialize the Slack client using your connection name from autokitteh.yaml.
# The connection name "slack_conn" must match what's defined in your YAML.
slack = slack_client("slack_conn")


def on_slack_message(event):
    """Handle incoming Slack messages.

    This function runs every time someone sends a message in Slack.
    The 'event' parameter contains all the message details from Slack.
    """
    print("=== New Slack Message Received ===")

    try:
        # Get the important parts of the message.
        message_text = event.data.get("text", "")
        user_id = event.data.get("user", "")
        channel_id = event.data.get("channel", "")

        print(f"Message: {message_text}")
        print(f"From: {user_id}")
        print(f"Channel: {channel_id}")

        # Respond to simple commands
        if "hello" in message_text.lower():
            print("User said hello! Responding with greeting.")
            # To actually send a response:
            # slack.chat_postMessage(
            #     channel=channel_id,
            #     text="Hello! 👋 Nice to meet you!"
            # )

        elif "help" in message_text.lower():
            print("User needs help! Sending help message.")
            # To send help:
            # slack.chat_postMessage(
            #     channel=channel_id,
            #     text="I can respond to 'hello' and 'help' commands!"
            # )

        else:
            print("Regular message - just logging it.")

        return {"status": "success"}
    # Handle exceptions gracefully
    except AttributeError as e:
        print(f"Error processing message: {e}")
        return {"status": "error", "message": str(e)}
    except KeyError as e:
        print(f"Missing expected key: {e}")
        return {"status": "error", "message": f"Missing key: {e}"}

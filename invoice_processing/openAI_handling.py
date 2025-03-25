"""Functions to create AI files, create threads, and send requests to the OpenAI API."""

import base64
import binascii
import io
import time

import autokitteh
from autokitteh.openai import openai_client
import requests


chatgpt = openai_client("openai_conn")


def create_ai_file(attachment, vector_store_id):
    """Create an AI file from an attachment for OpenAI processing."""
    try:
        if attachment["data"].startswith("data:"):
            # Extract base64 data after the comma.
            _, data = attachment["data"].split(",", 1)
            file_data = base64.b64decode(data)
        else:
            # Handle regular base64 data.
            file_data = base64.b64decode(attachment["data"])

        file_stream = io.BytesIO(file_data)
        file_stream.name = attachment["filename"]

        file_stream.seek(0)

        # Create file for assistant.
        message_file = chatgpt.files.create(file=file_stream, purpose="assistants")
        file_stream.close()
        return message_file

    except ValueError as e:
        print(f"Error creating AI file: {str(e)}")
        return None


def create_thread(content, attachments, assistant, response_schema):
    """Create an OpenAI thread, run the assistant, and get the response."""
    try:
        # Create thread with user message.
        thread = chatgpt.beta.threads.create(
            messages=[
                {
                    "role": "user",
                    "content": content,
                    "attachments": attachments,
                }
            ]
        )

        # Run the assistant on the thread.
        run = chatgpt.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant.id,
            response_format=response_schema,
        )

        # Poll for completion.
        while True:
            run_status = chatgpt.beta.threads.runs.retrieve(
                thread_id=thread.id, run_id=run.id
            )
            if run_status.status == "completed":
                break
            elif run_status.status in ["failed", "cancelled", "expired"]:
                print(f"Run failed - {run_status.status}")
                return None

            time.sleep(5)  # Reduced polling interval.

        # Get the assistant's response.
        ai_messages = chatgpt.beta.threads.messages.list(thread_id=thread.id)

        assistant_message = next(
            (msg for msg in ai_messages.data if msg.role == "assistant"), None
        )

        if assistant_message and assistant_message.content:
            return assistant_message.content[0].text.value

    except requests.exceptions.RequestException as e:
        print(f"Network error: {str(e)}")

    return None


@autokitteh.activity
def send_ai_request(
    message_body, message_attachments, message_images, ai_request, response_schema
):
    """Send a request to the OpenAI API with message content and attachments"""
    # Early return if no content to analyze.
    if not message_body and not message_attachments and not message_images:
        print("No content to analyze")
        return False

    # Create a temporary file from the message body.
    temp_file_path = f"message_{int(time.time())}.txt"
    temp_file = {
        "filename": temp_file_path,
        "data": base64.b64encode(message_body.encode("utf-8")).decode("utf-8"),
    }

    # Create assistant with explicit model version.
    assistant = chatgpt.beta.assistants.create(
        name="Document Analyzer",
        instructions=ai_request,
        model="gpt-4o",  # Use latest model.
        tools=[{"type": "file_search"}],
    )

    # Create vector store for file search.
    vector_store = chatgpt.vector_stores.create(name="Invoice Analysis")

    # Process all files (message body and attachments).
    messages = []

    temp_ai_file = create_ai_file(temp_file, vector_store.id)
    if temp_ai_file:
        messages.append(temp_ai_file)

    for attachment in message_attachments:
        ai_file = create_ai_file(attachment, vector_store.id)
        if ai_file:
            messages.append(ai_file)

    attachments = [
        {"file_id": file.id, "tools": [{"type": "file_search"}]} for file in messages
    ]

    # Prepare content array with instructions.
    content = [{"type": "text", "text": ai_request}]

    # Handle image processing if present.
    if message_images and len(message_images) > 0:
        try:
            image_data = message_images[0]["data"]
            if image_data.startswith("data:"):
                _, base64_data = image_data.split(",", 1)
                image_bytes = base64.b64decode(base64_data)

                image_stream = io.BytesIO(image_bytes)
                image_stream.name = "image.png"

                file = chatgpt.files.create(file=image_stream, purpose="vision")

                content.append(
                    {"type": "image_file", "image_file": {"file_id": file.id}}
                )
                print(f"Image added with file ID: {file.id}")
        except binascii.Error as e:
            print(f"Base64 decoding error: {str(e)}")
        except OSError as e:
            print(f"IO error processing image: {str(e)}")

    # Create thread and get response.
    result = create_thread(content, attachments, assistant, response_schema)
    return result

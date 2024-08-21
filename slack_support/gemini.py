import os
import json

import google.generativeai as genai

# How do i know if this is "picklable" or not? It has no return value? Do I need to run this every time?
# Is this running in an activity?
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Make this run every time outside of an activity if it's in global scope?
model = genai.GenerativeModel(
    "gemini-1.5-flash",
    generation_config={"response_mime_type": "application/json"},
)


def extract_topic(text: str, topics: set[str]) -> str:
    prompt = f"""Topics: {', '.join(topics)}
Is the following text a request for help with one of these topics?
Example responses:
If a request for help and a topic from the list: {{"help": true, "topic": "cats" }}
If a request for help and topic is not from the list: {{"help": true, "topic": None }}
If not a request for help: {{"help": false}}

Text to analyze:
{text}"""

    resp = json.loads(model.generate_content(prompt).text)
    return resp.get("help"), resp.get("topic")

"""Deduce the topic of a given text."""

import json

from autokitteh.google import gemini_client


generation_config = {"response_mime_type": "application/json"}
gemini = gemini_client("gemini_conn", generation_config=generation_config)


def extract_topic(text: str, topics: set[str]) -> str:
    prompt = f"""Topics: {", ".join(topics)}
        Is the following text a request for help with one of these topics?
        Example responses:
        If a request for help and a topic is in the list:
        {{"help": true, "topic": "cats" }}
        If a request for help and topic is not in the list:
        {{"help": true, "topic": None }}
        If not a request for help: {{"help": false}}

        Text to analyze:
        {text}"""

    resp = json.loads(gemini.generate_content(prompt).text)
    return resp.get("help"), resp.get("topic")

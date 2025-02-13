import json
import re

from autokitteh.google import gemini_client


MODEL = "gemini-1.5-flash"
gemini = gemini_client("gemini_conn", model_name=MODEL)


def extract_topic(text: str, topics: set[str]) -> str:
    prompt = f"""Topics: {", ".join(topics)}
Is the following text a request for help with one of these topics?
Example responses:
If a request for help and a topic from the list: {{"help": true, "topic": "cats" }}
If a request for help and topic is not from the list: {{"help": true, "topic": None }}
If not a request for help: {{"help": false}}

Text to analyze:
{text}"""

    response_text = gemini.generate_content(prompt).text.strip()

    # Remove markdown code block markers (```json and ```)
    response_text = re.sub(r"^```json\n?|```$", "", response_text).strip()

    try:
        resp = json.loads(response_text)
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON response: {response_text}") from None

    return resp.get("help"), resp.get("topic")

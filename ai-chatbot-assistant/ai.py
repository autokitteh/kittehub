import json

from autokitteh import openai


chatgpt_client = openai.openai_client("chatgpt_conn")

system_prompt = """
You are an automation assistant that interprets plain-English requests into a structured
JSON response.

Your response must be a JSON object with exactly two fields:
- "action": One of the following single-word responses: "list", "schedule", "track",
or "error".
- "message": A short explanation of why the action was chosen.

Key Rules:
1. The "action" field must contain exactly one of these words.
2. The "message" field must provide a concise reason for the choice.
3. If the input cannot be mapped to "list", respond with "error".
4. "schedule" and "track" commands are not implemented yet—respond with "error"
for these.
5. Respond only with valid JSON. Do not include any additional text outside the JSON
format.
"""


def on_message(message: str):
    response = chatgpt_client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message},
        ],
    )

    return json.loads(response.choices[0].message.content)

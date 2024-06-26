"""
When receiving a new email, ask read its content/summary and ask Chat GPT to categorize it 
(e.g. related to technical work, or marketing, sales, etc.) - and as a result, send a 
message to Slack channel based on the category, and/or label the message in Gmail
"""
load("@chatgpt", "my_chatgpt")
load("@gmail", "my_gmail")
load("@http", "my_http")
load("@slack", "my_slack")

def on_http_get():
    _poll_inbox()
    _ask_gpt()
    _send_slack_message()

def _poll_inbox():
    resp = my_gmail.messages_list(max_results = 10, q = "is:unread")
    if resp.error:
        fail("Error: " + resp.error)
    if resp.http_status_code != 200:
        fail("Error: HTTP response code %d" % resp.http_status_code)
    print(resp)

def _ask_gpt():
    # Example 1: trivial interaction with ChatGPT.
    resp = my_chatgpt.create_chat_completion(message = "Hello!")

    # For educational and debugging purposes, print ChatGPT's response
    # in the AutoKitteh session's log.
    print(resp)

def _send_slack_message():
    my_slack.chat_post_message(channel = "pasha-slack-test", text = "Hello, world!")

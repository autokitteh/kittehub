import os
import requests
import time
import urllib.parse

from autokitteh.slack import slack_client


slack = slack_client("slack_connection")
SLACK_CHANNEL = os.getenv("SLACK_CHANNEL")


def on_command(event):
    topic = event.data.text  # Extract the topic from the Slack command
    existing_articles = set()
    fetch_articles(topic, existing_articles)

    while True:
        all_articles = set(existing_articles)
        fetch_articles(topic, all_articles)
        new_articles = all_articles - existing_articles

        if new_articles:
            for article in new_articles:
                _, title, url = article
                s_message = f"Title: {title}, URL: {url if url else 'No URL'}"
                print(s_message)
                slack.chat_postMessage(channel=SLACK_CHANNEL, text=s_message)
            existing_articles.update(new_articles)

        time.sleep(120)


def fetch_articles(topic, all_articles):
    encoded_query = urllib.parse.quote(topic)
    full_url = f"http://hn.algolia.com/api/v1/search_by_date?query={encoded_query}&tags=story&page=0"
    response = requests.get(full_url).json()
    hits = response["hits"]

    # Extract some of the article fields from API response
    for article in hits:
        object_id = article["objectID"]
        title = article["title"]
        url = article.get("url")
        all_articles.add((object_id, title, url))

"""A simple workflow that is triggered by a webhook."""


def on_webhook(event):
    print(event)

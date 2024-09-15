"""This module demonstrates the usage of AutoKitteh webhooks."""

import os

import basic_auth
import bearer_token
import no_auth


BASE_URL = os.getenv("HTTPBIN_BASE_URL")  # Set in "autokitteh.yaml".


def on_http_get_or_head(event):
    """Handle incoming HTTP GET and HEAD requests.

    - https://www.rfc-editor.org/rfc/rfc9110#name-get
    - https://www.rfc-editor.org/rfc/rfc9110#name-head

    Args:
        event: Incoming HTTP request details.
    """
    _print_request_details(event.data)

    print("Query parameters:")
    if not event.data.url.query:
        print("  none")
    for key in sorted(event.data.url.query):
        print(f"  {key} = {event.data.url.query[key]}")


def on_http_post_form(event):
    """Handle URL-encoded form submissions in HTTP POST requests.

    - https://www.rfc-editor.org/rfc/rfc9110#name-post
    - https://html.spec.whatwg.org/multipage/forms.html

    Args:
        event: Incoming HTTP request details.
    """
    _print_request_details(event.data)
    print(f"Body: {event.data.body.bytes}")

    print("Form parameters:")
    if not event.data.body.form:
        print("  none")
    for key in sorted(event.data.body.form):
        print(f"  {key} = {event.data.body.form[key]}")


def on_http_post_json(event):
    """Handle incoming HTTP POST requests with a JSON body.

    https://www.rfc-editor.org/rfc/rfc9110#name-post

    Args:
        event: Incoming HTTP request details.
    """
    _print_request_details(event.data)
    print(f"Body: {event.data.body.bytes}")
    print(f"JSON: {event.data.body.json}")


def _print_request_details(data):
    print(f"Triggered by an HTTP {data.method} request")
    print("Full URL:", data.raw_url)
    print("URL path:", data.url.path)

    print("Headers:")
    for key in sorted(data.headers):
        print(f"  {key} = {data.headers[key]}")


def send_requests(event):
    """Send various HTTP requests with various authentication schemes."""
    no_auth.send_requests(BASE_URL)
    basic_auth.send_requests(BASE_URL)
    bearer_token.send_requests(BASE_URL)

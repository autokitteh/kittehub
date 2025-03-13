"""This module demonstrates the "requests" library with an OAuth bearer token."""

from urllib.parse import urljoin

import requests


def send_requests(base_url):
    """Send HTTP requests with an OAuth bearer token.

    See: https://datatracker.ietf.org/doc/html/rfc6750
    """
    print("\n>>> Sending HTTP requests with an OAuth bearer token")

    url = urljoin(base_url, "bearer")
    token = "my_bearer_token"  # noqa: S105
    headers = {"Authorization": "Bearer " + token}
    resp = requests.get(url, headers=headers, timeout=10)
    _print_response_details(resp)


def _print_response_details(resp):
    print("Response URL:", resp.url)
    print("Response status code:", resp.status_code)
    print("Response text:", resp.text)
    print("Response headers:")
    for key in sorted(resp.headers):
        print(f"  {key} = {resp.headers[key]}")

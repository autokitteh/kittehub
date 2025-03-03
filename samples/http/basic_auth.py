"""This module demonstrates the "requests" library with basic authentication."""

import base64
from urllib.parse import urljoin

import requests


def send_requests(base_url):
    """Send HTTP requests with basic authentication (username + password).

    See: https://datatracker.ietf.org/doc/html/rfc7617
    """
    print("\n>>> Sending HTTP requests with basic authentication")

    expected_creds = ("user", "pass")
    url = urljoin(base_url, f"basic-auth/{expected_creds[0]}/{expected_creds[1]}")

    print("\n--- Use the expected credentials (authentication success)")
    resp = requests.get(url, auth=expected_creds, timeout=10)
    _print_response_details(resp)

    print("\n--- Use unexpected credentials (authentication failure)")
    # Also, set them directly in the HTTP request headers, instead of
    # using the "auth" parameter, just for the sake of demonstration.
    unexpected_creds = "someone_else:wrong_password"
    headers = {
        "Authorization": "Basic " + base64.b64encode(unexpected_creds.encode()).decode()
    }
    resp = requests.get(url, headers=headers, timeout=10)
    _print_response_details(resp)


def _print_response_details(resp):
    print("Response URL:", resp.url)
    print("Response status code:", resp.status_code)
    print("Response text:", resp.text)
    print("Response headers:")
    for key in sorted(resp.headers):
        print(f"  {key} = {resp.headers[key]}")

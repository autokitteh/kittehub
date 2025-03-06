"""This module demonstrates the "requests" library without authentication."""

from urllib.parse import urljoin

import requests


def send_requests(base_url):
    print(">>> Sending requests without authentication")

    _get_echo_params(base_url)
    _get_html(base_url)
    _get_json(base_url)
    _get_error(base_url)

    url = urljoin(base_url, "post")
    _post_echo_form(url)
    _post_echo_json(url)


def _get_echo_params(base_url):
    """https://httpbin.org/#/HTTP_Methods/get_get"""
    url = urljoin(base_url, "get")
    print(f"\n--- GET {url}")
    resp = requests.get(url, params={"key1": "value1", "key2": "value2"}, timeout=10)
    # Expected: "Content-Type" header is "application/json".
    _print_response_status_and_headers(resp)

    # httpbin echoes back query params (as "args"), headers, and other things
    # in the response's JSON body. In this specific case, the "headers",
    # "args", "url" keys should be present in the response body.

    # Expected JSON: {"args": {"key1": "value1", ... }, ...}
    print(f"Response body (JSON):\n{resp.json()}")
    # Expected text: same as JSON, but formatted as multiline text.
    print(f"Response body (text):\n{resp.text}")


def _get_html(base_url):
    """https://httpbin.org/#/Response_formats/get_html"""
    url = urljoin(base_url, "html")
    print(f"\n--- GET {url}")
    resp = requests.get(url, timeout=10)
    _print_response_status_and_headers(resp)

    # Expected text: "\u003c!DOCTYPE html\u003e\\n..."
    print(f"Response body (text):\n{resp.text}")
    # Don't call resp.json(), since HTML is not valid JSON.


def _get_json(base_url):
    """https://httpbin.org/#/Response_formats/get_json"""
    url = urljoin(base_url, "json")
    print(f"\n--- GET {url}")
    resp = requests.get(url, timeout=10)
    _print_response_status_and_headers(resp)

    # Expected text: same as JSON, but formatted as multiline byte text.
    print(f"response body (bytes):\n{resp.content}")
    # Expected JSON: {"slideshow": {"author": "Yours Truly", ... }}
    print(f"response body (json):\n{resp.json()}")
    # Expected value inside JSON: "Yours Truly".
    slideshow_author = resp.json().get("slideshow", {}).get("author")
    print("response_json['slideshow']['author']:", slideshow_author)


def _get_error(base_url):
    url = urljoin(base_url, "status/404")
    print(f"\n--- GET {url}")
    resp = requests.get(url, timeout=10)
    _print_response_status_and_headers(resp)  # Expected status code: 404.


def _post_echo_form(url):
    """https://httpbin.org/#/HTTP_Methods/post_post"""
    print(f"\n--- POST {url} (form)")
    resp = requests.post(url, data={"foo": "bar"}, timeout=10)
    # Expected: "Content-Type" header is "application/json".
    _print_response_status_and_headers(resp)

    # The form we submitted will be echoed back by httpbin under the "form" key.

    # Expected JSON: {..., "form": {"foo": "bar"}, ...}
    print(f"Response body (JSON):\n{resp.json()}")
    # Expected text: same as JSON, but formatted as multiline text.
    print(f"Response body (text):\n{resp.text}")


def _post_echo_json(url):
    """https://httpbin.org/#/HTTP_Methods/post_post"""
    print(f"\n--- POST {url} (JSON)")

    # Option 1: use the "json" param, without specifying content type.
    resp = requests.post(url, json={"foo": "bar"}, timeout=10)

    # Option 2: use the "data" param, and specify its content type.
    # headers={"Content-Type": "application/json", ...}
    # resp = requests.post(url, data={"foo": "bar"}, headers=headers)

    _print_response_status_and_headers(resp)

    # The JSON we sent will be echoed back by httpbin under the "data" key
    # (as a string), and the "json" key.

    # Expected JSON: {..., "data": "{...}", "json": {"foo": "bar"}, ...}
    print(f"Response body (JSON):\n{resp.json()}")
    # Expected text: same as JSON, but formatted as text.
    print(f"Response body (text):\n{resp.text}")


def _print_response_status_and_headers(resp):
    print("Response status code:", resp.status_code)
    print("Response headers:")
    for key in sorted(resp.headers):
        print(f"  {key} = {resp.headers[key]}")

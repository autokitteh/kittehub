"""gocat handlers.

This module provides webhook handlers for the gocat URL shortener/redirector service.
It processes incoming webhook requests and redirects them to stored URLs based on path
matching.
"""

from urllib.parse import urljoin

from autokitteh import Event, http_outcome
import store


def _extract_suffix(path: str) -> str:
    """Extract the suffix portion from a webhook path.

    The expected path format is: /webhooks/<slug>/<suffix>
    This function extracts and returns the <suffix> part.

    >>> _extract_suffix("/webhooks/myslug/docs/api")
    "docs/api"
    >>> _extract_suffix("/webhooks/myslug")
    ""

    Args:
        path: The full URL path from the webhook request

    Returns:
        The suffix portion of the path (everything after the slug), or empty string if
        no suffix

    Raises:
        ValueError: If the path doesn't have at least 2 parts when split by '/'
    """
    # Remove leading slash if present
    if path.startswith("/"):
        path = path[1:]

    # Split path into parts: ['webhooks', '<slug>', '<suffix>']
    parts = path.split("/", 2)
    if len(parts) < 2:
        raise ValueError("Invalid path, expecting /webhooks/<slug>/<suffix>")

    # Return suffix (third part) if it exists, otherwise empty string
    return parts[2] if len(parts) > 2 else ""


def on_webhook(event: Event):
    """Handle incoming webhook events and redirect to stored URLs.

    This is the main webhook handler that processes incoming requests and performs
    URL lookups and redirections based on the path suffix.

    Behavior:
    - No suffix: Redirects to the Google Spreadsheet (302)
    - One match: Redirects to the matched URL (302)
    - Multiple matches: Returns an HTML page with all matching links (200)
    - No matches: Returns 404 error
    """
    # Extract the suffix from the URL path (everything after the slug)
    suffix = _extract_suffix(event.data.url.path)

    print(f"path suffix: '{suffix}'")

    if not suffix:
        # Redirect to the spreadsheet URL if no suffix is provided.
        loc = store.spreadsheet_url()
        print(f"no suffix provided, redirecting to {loc}")
        http_outcome(302, headers={"Location": loc})
        return

    # Split the suffix into first part (search key) and remaining path
    parts = suffix.split("/", 1)

    # first = the search key to look up in the store
    # second = any additional path to append to the matched URL
    first, second = parts[0], parts[1] if len(parts) > 1 else ""

    # Search for matching URLs in the store
    results = store.find(first)

    match results:
        case []:
            print("no matches found")
            http_outcome(404, body="No matches found")
            return

        case [result]:
            # If there's an additional path, append it to the result URL
            if second:
                # Ensure the base URL ends with a slash before joining
                if not result.endswith("/"):
                    result += "/"
                loc = urljoin(result, second)
            else:
                loc = result

            print(f"single match found: {result} -> {loc}")

            http_outcome(302, headers={"Location": loc})
            return

        case _:
            print("multiple matches found:\n- " + "\n- ".join(results))

            links = "\n\t\t".join(
                f'<li><a href="{url}">{url}</a></li>' for url in results
            )

            body = f"""<html>
    <head>
        <title>Multiple matches</title>
    </head>
    <body>
        <h1>Multiple matches for '{first}'</h1>
        <ul>
            {links}
        </ul>
    </body>
</html>"""

            http_outcome(200, body=body, headers={"Content-Type": "text/html"})
            return

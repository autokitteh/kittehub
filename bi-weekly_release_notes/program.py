"""Automated bi-weekly release notes generation workflow."""

from datetime import datetime, UTC
import os
import html
import base64

from autokitteh.atlassian import confluence_client, jira_client
from autokitteh.openai import openai_client
from autokitteh.google import gmail_client

# Configuration
JIRA_FILTER_ID = os.getenv("JIRA_FILTER_ID", "Last Two Weeks Deliveries")
CONFLUENCE_SPACE_KEY = os.getenv("CONFLUENCE_SPACE_KEY", "PRODUCT")
CONFLUENCE_PARENT_PAGE_ID = os.getenv("CONFLUENCE_PARENT_PAGE_ID", "")
JIRA_SERVER_URL = os.getenv(
    "JIRA_SERVER_URL", "https://your-jira-instance.atlassian.net"
)
CONFLUENCE_SERVER_URL = os.getenv(
    "CONFLUENCE_SERVER_URL", "https://your-confluence-instance.atlassian.net"
)
NOTIFICATION_EMAIL = os.getenv("NOTIFICATION_EMAIL", "")

# Clients
jira = jira_client("jira_conn")
confluence = confluence_client("conf_conn")
chatgpt = openai_client("chatgpt_conn")
gmail = gmail_client("gmail_conn").users()


def generate_release_notes(_):
    """Main workflow entry point."""
    print("Starting release notes generation...")

    tickets = fetch_jira_tickets()
    if not tickets:
        print("No tickets found.")
        return

    print(f"Processing {len(tickets)} tickets...")
    features, bug_fixes = categorize_tickets(tickets)

    processed_features = [process_ticket(t) for t in features]
    processed_bug_fixes = [process_ticket(t) for t in bug_fixes]

    title = "Release Notes - " + datetime.now(tz=UTC).strftime("%B - %d - %Y - %H:%M")
    page = create_confluence_page(title, processed_features, processed_bug_fixes)

    if NOTIFICATION_EMAIL and page:
        page_url = get_page_url(page)
        if page_url:
            send_email(
                title, page_url, len(processed_features), len(processed_bug_fixes)
            )
        else:
            print("Could not determine page URL - skipping email notification")

    print(f"Done: {title}")


def fetch_jira_tickets():
    """Fetch tickets from JIRA filter."""
    jql = (
        f'filter = "{JIRA_FILTER_ID}"'
        if not JIRA_FILTER_ID.isdigit()
        else f"filter = {JIRA_FILTER_ID}"
    )

    result = jira.post(
        "/rest/api/3/search/jql",
        json={
            "jql": jql,
            "maxResults": 100,
            "fields": ["key", "summary", "issuetype", "description"],
        },
    )
    tickets = result.get("issues", []) if isinstance(result, dict) else result
    print(f"Fetched {len(tickets)} tickets")
    return tickets


def categorize_tickets(tickets):
    """Split tickets into features and bug fixes."""
    bug_types = {"bug", "defect", "hotfix"}
    features, bugs = [], []

    for ticket in tickets:
        issue_type = (
            ticket.get("fields", {}).get("issuetype", {}).get("name", "").lower()
        )
        (bugs if issue_type in bug_types else features).append(ticket)

    print(f"Categorized: {len(features)} features, {len(bugs)} bugs")
    return features, bugs


def process_ticket(ticket):
    """Process a single ticket with AI summary."""
    key = ticket.get("key", "UNKNOWN")
    summary = ticket.get("fields", {}).get("summary", "No summary")
    jira_url = getattr(jira, "server_url", JIRA_SERVER_URL)

    try:
        ai_summary = generate_ai_summary(ticket)
    except Exception as e:  # noqa: BLE001
        print(f"Error summarizing {key}: {e}")
        ai_summary = "Summary unavailable"

    return {
        "key": key,
        "summary": summary,
        "ai_description": ai_summary,
        "url": f"{jira_url}/browse/{key}",
    }


def generate_ai_summary(ticket):
    """Generate AI summary for a ticket."""
    summary = ticket["fields"]["summary"]
    description = ticket["fields"].get("description", "No description")

    prompt = f"""Provide a concise 2-3 sentence summary for release notes:

Title: {summary}
Description: {description}

Focus on what was delivered/fixed and business value."""

    response = chatgpt.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a technical writer creating release notes.",
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=150,
        temperature=0.3,
    )

    return response.choices[0].message.content.strip()


def create_confluence_page(title, features, bug_fixes):
    """Create Confluence page with release notes."""
    content = build_content(features, bug_fixes)

    space_id = get_space_id()
    if space_id:
        payload = {
            "spaceId": space_id,
            "status": "current",
            "title": title,
            "body": {"representation": "storage", "value": content},
        }
        if CONFLUENCE_PARENT_PAGE_ID:
            payload["parentId"] = CONFLUENCE_PARENT_PAGE_ID

        result = confluence.post("/wiki/api/v2/pages", json=payload)
        print(f"Created page: {title}")
        return result

    # Fallback to API v1
    payload = {
        "type": "page",
        "title": title,
        "space": {"key": CONFLUENCE_SPACE_KEY},
        "body": {"storage": {"value": content, "representation": "storage"}},
    }
    if CONFLUENCE_PARENT_PAGE_ID:
        payload["ancestors"] = [{"id": CONFLUENCE_PARENT_PAGE_ID}]

    result = confluence.post("/rest/api/content", json=payload)
    print(f"Created page: {title}")
    return result


def get_space_id():
    """Get space ID from space key."""
    space = confluence.get(f"/rest/api/space/{CONFLUENCE_SPACE_KEY}")
    return space.get("id")


def get_page_url(page):
    """Extract page URL from API response."""
    if "webui" in page.get("_links", {}):
        return page["_links"]["webui"]
    if "id" in page:
        base = getattr(confluence, "server_url", CONFLUENCE_SERVER_URL)
        return f"{base}/wiki/spaces/{CONFLUENCE_SPACE_KEY}/pages/{page['id']}"


def build_content(features, bug_fixes):
    """Build HTML content for Confluence page."""
    now = datetime.now(tz=UTC)
    content = f"""<h1>Release Notes - {now.strftime("%B %d, %Y")}</h1>
<p>This release includes the following updates and improvements:</p>"""

    if features:
        content += "<h2>🚀 New Features & Deliverables</h2><ul>"
        content += "".join(build_ticket_html(f) for f in features)
        content += "</ul>"

    if bug_fixes:
        content += "<h2>🐛 Bug Fixes</h2><ul>"
        content += "".join(build_ticket_html(b) for b in bug_fixes)
        content += "</ul>"

    if not features and not bug_fixes:
        content += "<p><em>No tickets found for this release period.</em></p>"

    content += (
        f"<hr/><p><em>Generated on {now.strftime('%Y-%m-%d at %H:%M UTC')}</em></p>"
    )
    return content


def build_ticket_html(ticket):
    """Build HTML for a single ticket."""
    escaped_summary = html.escape(ticket["summary"])
    escaped_desc = html.escape(ticket["ai_description"])
    return f"""<li>
<strong><a href="{ticket["url"]}">{ticket["key"]}</a>: {escaped_summary}</strong>
<br/>{escaped_desc}
</li>"""


def send_email(title, url, feature_count, bug_count):
    """Send email notification."""
    profile = gmail.getProfile(userId="me").execute()

    body = f"""Hi there!

New release notes have been published:

📋 Title: {title}
🔗 Link: {url}

📊 Summary:
• {feature_count} new features and deliverables
• {bug_count} bug fixes

Best regards,
Automated Release Notes System

---
Generated on {datetime.now(tz=UTC).strftime("%Y-%m-%d at %H:%M UTC")}"""

    message = f"""From: {profile["emailAddress"]}
To: {NOTIFICATION_EMAIL}
Subject: New Release Notes Published: {title}

{body}"""

    encoded = base64.urlsafe_b64encode(message.encode()).decode()
    gmail.messages().send(userId="me", body={"raw": encoded}).execute()
    print(f"Email sent to {NOTIFICATION_EMAIL}")

"""Defines metadata schema, allowed integrations, and categories.

- METADATA: Required metadata fields in README files.
- INTEGRATIONS: List of allowed integration values.
- CATEGORIES: List of allowed category values.
"""

METADATA = ["title", "description", "integrations", "categories"]

INTEGRATIONS = [
    "slack",
    "hubspot",
    "auth0",
    "aws",
    "gmail",
    "twilio",
    "drive",
    "sheets",
    "docs",
    "calendar",
    "chatgpt",
    "confluence",
    "jira",
    "http",
    "sqlite3",
    "github",
    "githubcopilot",
    "asana",
    "forms",
    "googlegemini",
]

CATEGORIES = [
    "DevOps",
    "Reliability",
    "Samples",
    "CRM",
    "AI",
    "Productivity",
    "Office Automation",
    "Durability",
]

"""This program demonstrates AutoKitteh's 2-way Google Forms integration.

API documentation:
- https://docs.autokitteh.com/integrations/google/forms/python
- https://docs.autokitteh.com/integrations/google/forms/events
"""

import json
import os
from pathlib import Path

from autokitteh.google import google_forms_client


def add_question(event):
    """Add a new question to the form that our connection watches.

    This is the same as Google's quickstart code sample, but simpler:
    https://github.com/googleworkspace/python-samples/tree/main/forms
    """
    # Get the form that our connection watches.
    forms = google_forms_client("forms_conn").forms()
    form_id = os.environ.get("forms_conn__FormID")
    form = forms.get(formId=form_id).execute()
    new_index = len(form["items"])

    # Add a new question to the form.
    body = Path("new_question.json").read_text().replace("0", str(new_index))
    result = forms.batchUpdate(formId=form_id, body=json.loads(body)).execute()
    print(result)


def on_form_change(event):
    title = event.data.form.info.title
    form_id = event.data.form_id
    revision = event.data.form.revision_id
    items = len(event.data.form.get("items", []))
    print(f"Form change: {title} ({form_id}), revision {revision}, {items} items")


def on_form_response(event):
    print("New form response submitted:", event.data)

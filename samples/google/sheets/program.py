"""This program demonstrates AutoKitteh's 2-way Google Sheets integration.

API documentation:
https://docs.autokitteh.com/integrations/google/sheets/python
"""

import autokitteh
from autokitteh.google import google_id, google_sheets_client
from autokitteh.slack import slack_client


sheet = google_sheets_client("sheets_conn").spreadsheets().values()
slack = slack_client("slack_conn")


def on_slack_slash_command(event):
    """Use a Slack slash command to interact with a Google Sheet.

    See: https://api.slack.com/interactivity/slash-commands, and
    https://api.slack.com/interactivity/handling#message_responses

    In this sample, we expect the slash command's text to be either:
    - A Google Sheets ID (https://developers.google.com/sheets/api/guides/concepts)
    - A full Google Sheets URL (to extract the spreadsheet ID from it)

    Args:
        event: Slack event data.
    """
    user_id = event.data.user_id
    sheet_id = _extract_sheet_id(event.data.text, user_id)
    if not sheet_id:
        return

    _write_values(sheet_id, user_id)
    _read_values(sheet_id, user_id)
    _read_formula(sheet_id, user_id)


def _extract_sheet_id(text, user_id):
    """Extract a Google Sheets ID from a Slack slash command."""
    try:
        return google_id(text)
    except ValueError:
        msg = f"Invalid Google Sheets URL or spreadsheet ID: `{text}`"
        slack_client("slack_conn").chat_postMessage(channel=user_id, text=msg)
        return None


@autokitteh.activity
def _write_values(spreadsheet_id, slack_target):
    """Write multiple cell values, with different data types."""
    resp = sheet.update(
        spreadsheetId=spreadsheet_id,
        # Explanation of the A1 notation for cell ranges:
        # https://developers.google.com/sheets/api/guides/concepts#expandable-1
        range="Sheet1!A1:B7",
        # Value input options:
        # https://developers.google.com/sheets/api/reference/rest/v4/ValueInputOption
        valueInputOption="USER_ENTERED",
        body={
            "values": [
                ["String", "Hello, world!"],
                ["Number", -123.45],
                ["Also number", "-123.45"],
                ["Percent", "10.12%"],
                ["Boolean", True],
                ["Date", "2022-12-31"],
                ["Formula", "=B2*B3"],
            ]
        },
    ).execute()

    text = f"Updated: range `{resp['updatedRange']!r}`, `{resp['updatedRows']}` rows, "
    text += f"`{resp['updatedColumns']}` columns, `{resp['updatedCells']}` cells"
    slack.chat_postMessage(channel=slack_target, text=text)


@autokitteh.activity
def _read_values(id, slack_target):
    """Read multiple cell values from a Google Sheet, and send them to Slack.

    Value render options:
    https://developers.google.com/sheets/api/reference/rest/v4/ValueRenderOption
    """
    # Default value render option: "FORMATTED_VALUE".
    resp = sheet.get(spreadsheetId=id, range="A1:B6").execute()
    col_a, formatted_col_b = list(zip(*resp.get("values", [])))

    ufv = "UNFORMATTED_VALUE"
    resp = sheet.get(spreadsheetId=id, range="A1:B6", valueRenderOption=ufv).execute()
    unformatted_col_b = [v for _, v in resp.get("values", [])]

    for i, row in enumerate(zip(col_a, formatted_col_b, unformatted_col_b)):
        data_type, formatted, unformatted = row
        text = "Row {0}: {1} = formatted `{2!r}`, unformatted `{3!r}`"
        text = text.format(i + 1, data_type, formatted, unformatted)
        slack.chat_postMessage(channel=slack_target, text=text)


@autokitteh.activity
def _read_formula(id, slack_target):
    """Read a single cell value with a formula, and its evaluated result.

    Value render options:
    https://developers.google.com/sheets/api/reference/rest/v4/ValueRenderOption
    """
    f = "FORMULA"
    resp = sheet.get(spreadsheetId=id, range="B7", valueRenderOption=f).execute()
    value = resp.get("values", [["Not found"]])[0][0]
    slack.chat_postMessage(channel=slack_target, text=f"Formula: `{value!r}`")

    # Default value render option: "FORMATTED_VALUE".
    resp = sheet.get(spreadsheetId=id, range="B7").execute()
    value = resp.get("values", [["Not found"]])[0][0]
    slack.chat_postMessage(channel=slack_target, text=f"Formatted: `{value!r}`")

    ufv = "UNFORMATTED_VALUE"
    resp = sheet.get(spreadsheetId=id, range="B7", valueRenderOption=ufv).execute()
    value = resp.get("values", [["Not found"]])[0][0]
    slack.chat_postMessage(channel=slack_target, text=f"Unformatted: `{value!r}`")

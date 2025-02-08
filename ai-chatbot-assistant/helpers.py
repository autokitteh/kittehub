import os

import autokitteh
from autokitteh.google import google_sheets_client


sheets = google_sheets_client("googlesheets_conn")

SHEET_ID = os.getenv("SHEET_ID")


@autokitteh.activity
def get_sheets_data(sheet_name: str):
    """Get data from the specified Google Sheet.

    Args:
        sheet_name (str): The name of the sheet (tab).

    Returns:
        list: List of tuples containing (pr_number, author, body, url).
    """
    range_name = f"{sheet_name}!A:D"
    return (
        sheets.spreadsheets()
        .values()
        .get(spreadsheetId=SHEET_ID, range=range_name)
        .execute()
    )


@autokitteh.activity
def append_row_to_sheet(sheet_name: str, values: list):
    """Appends a row to the specified Google Sheet.

    Args:
        spreadsheet_id (str): The Google Spreadsheet ID.
        sheet_name (str): The name of the sheet (tab).
        values (list): List of tuples containing (pr_number, author, body, url).

    Returns:
        dict: API response.
    """
    range_name = f"{sheet_name}!A:D"  # Use columns A-D for the 4 values
    # Transform list of tuples into list of lists for the API
    formatted_values = [
        [str(comment_id), author, body, url] for comment_id, author, body, url in values
    ]
    body = {"values": formatted_values}

    # Append the rows
    sheets.spreadsheets().values().append(
        spreadsheetId=SHEET_ID,
        range=range_name,
        valueInputOption="RAW",
        insertDataOption="INSERT_ROWS",
        body=body,
    ).execute()


def format_messages_for_slack(rows):
    formatted_messages = []
    for row in rows["values"]:
        comment_id, author, body, url = row
        message = (
            f"*Comment ID:* {comment_id}\n"
            f"*Author:* {author}\n"
            f"*Message:* {body}\n"
            f"*URL:* {url}\n"
            "---"  # Add separator between messages
        )
        formatted_messages.append(message)

    return "\n".join(formatted_messages)

"""Log Discord message events and the author's username into a Google Sheet."""

import os

from autokitteh.google import google_sheets_client


SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
RANGE_NAME = os.getenv("RANGE_NAME")

sheet = google_sheets_client("googlesheets_conn").spreadsheets().values()


def on_discord_message(event):
    values = [[event.data["author"]["username"], event.data["content"]]]
    sheet.append(
        spreadsheetId=SPREADSHEET_ID,
        range=RANGE_NAME,
        valueInputOption="USER_ENTERED",
        body={"values": values},
    ).execute()

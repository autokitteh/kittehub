import os
from autokitteh.google import google_id, google_sheets_client
SPREAD_SHEET_ID = "1_yEEKKZn_0pbtnIKjD0OtKUhlrqKs5bmmfJIDaHCuSI"

def get_list_of_rooms():
    sheets = google_sheets_client("google_sheets_conn").spreadsheets().values()
    rows = sheets.get(spreadsheetId=os.getenv("SPREAD_SHEET_ID"), range="A:A").execute()
    values = rows.get('values', [])
    rooms = [cell[0] for cell in values if cell]
    return rooms
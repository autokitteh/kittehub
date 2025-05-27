"""Reads pairs of numbers from a Google Sheet and sends them to a SOAP calculator."""

import os

import autokitteh
from autokitteh.google import google_sheets_client
from zeep import Client


sheet = google_sheets_client("sheets_conn").spreadsheets().values()

SHEET_ID = os.getenv("SHEET_ID")
SHEET_RANGE = os.getenv("SHEET_RANGE")
SOAP_WSDL = os.getenv("SOAP_WSDL")

client = Client(SOAP_WSDL)


# activity is required because zeep methods lack __name__,
# causing AutoKitteh to fail with AttributeError.
@autokitteh.activity
def on_trigger(_):
    """Workflow entry point."""
    response = sheet.get(spreadsheetId=SHEET_ID, range=SHEET_RANGE).execute()
    rows = response.get("values", [])

    if not rows:
        print("No data found.")
        return

    for row in rows:
        a = int(row[0])
        b = int(row[1])

        result = client.service.Add(intA=a, intB=b)
        print(f"{a} + {b} = {result}")

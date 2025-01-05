"""This program demonstrates AutoKitteh's 2-way Google Sheets integration.

API documentation:
https://docs.autokitteh.com/integrations/google/sheets/python
"""

import autokitteh
from autokitteh.google import google_sheets_client


sheet = google_sheets_client("sheets_conn").spreadsheets().values()


def on_http_get(event):
    """Entry point for the workflow.

    This function expects the URL parameter 'id' to be a valid Google Sheets ID
    (see https://developers.google.com/sheets/api/guides/concepts).

    Example URL: "http://localhost:9980/webhooks/<webhook-slug>?id=<Google-Sheets-ID>"

    Args:
        event: HTTP event data, including URL query parameters.
    """
    sheet_id = event.data.url.query.get("id")
    if not sheet_id:
        print("Error: Missing required 'id' URL parameter for Google Sheets.")
        return

    _write_values(sheet_id)
    _read_values(sheet_id)
    _read_formula(sheet_id)


@autokitteh.activity
def _write_values(id):
    """Write multiple cell values, with different data types."""
    resp = sheet.update(
        spreadsheetId=id,
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

    print(f"Updated range: {resp['updatedRange']!r}")
    print(f"Rows: {resp['updatedRows']}")
    print(f"Columns: {resp['updatedColumns']}")
    print(f"Cells: {resp['updatedCells']}")


@autokitteh.activity
def _read_values(id):
    """Read multiple cell values from a Google Sheet, and send them to Slack.

    Value render options:
    https://developers.google.com/sheets/api/reference/rest/v4/ValueRenderOption
    """
    # Default value render option: "FORMATTED_VALUE".
    resp = sheet.get(spreadsheetId=id, range="A1:B6").execute()
    col_a, formatted_col_b = list(zip(*resp.get("values", []), strict=True))

    ufv = "UNFORMATTED_VALUE"
    resp = sheet.get(spreadsheetId=id, range="A1:B6", valueRenderOption=ufv).execute()
    unform_col_b = [v for _, v in resp.get("values", [])]

    for i, row in enumerate(zip(col_a, formatted_col_b, unform_col_b, strict=True)):
        data_type, formatted, unformatted = row
        text = f"Row {i + 1}: {data_type} = formatted "
        text += f"`{formatted!r}`, unformatted `{unformatted!r}`"
        print(text)


@autokitteh.activity
def _read_formula(id):
    """Read a single cell value with a formula, and its evaluated result.

    Value render options:
    https://developers.google.com/sheets/api/reference/rest/v4/ValueRenderOption
    """
    f = "FORMULA"
    resp = sheet.get(spreadsheetId=id, range="B7", valueRenderOption=f).execute()
    value = resp.get("values", [["Not found"]])[0][0]
    print(f"Formula: `{value!r}`")

    # Default value render option: "FORMATTED_VALUE".
    resp = sheet.get(spreadsheetId=id, range="B7").execute()
    value = resp.get("values", [["Not found"]])[0][0]
    print(f"Formula: `{value!r}`")

    ufv = "UNFORMATTED_VALUE"
    resp = sheet.get(spreadsheetId=id, range="B7", valueRenderOption=ufv).execute()
    value = resp.get("values", [["Not found"]])[0][0]
    print(f"Formula: `{value!r}`")

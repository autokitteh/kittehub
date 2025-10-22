"""Store module for managing URL mappings in Google Sheets.

This module provides an interface to a Google Spreadsheet that acts as a data store
for URL mappings. It reads short keys from column 1 and their corresponding full URLs
from column 2.

Required environment variables:
- GOOGLE_SPREADSHEET_ID: The ID of the Google Spreadsheet to use as the data store
- DIRECTORY_SHEET_NAME: (Optional) The name of the sheet to use. Defaults to the first
  sheet.
"""

from os import getenv

from autokitteh.google import gspread_client
import gspread


# Get the Google Spreadsheet ID from environment variable (required)
_GOOGLE_SPREADSHEET_ID = getenv("GOOGLE_SPREADSHEET_ID")
if not _GOOGLE_SPREADSHEET_ID:
    raise RuntimeError("GOOGLE_SPREADSHEET_ID not set")

# Get the sheet name from environment variable (optional, defaults to first sheet)
_DIRECTORY_SHEET_NAME = getenv("DIRECTORY_SHEET_NAME")

# Initialize the Google Sheets client and open the spreadsheet
_client = gspread_client("gsheets").open_by_key(_GOOGLE_SPREADSHEET_ID)


def spreadsheet_url() -> str:
    """Get the URL of the Google Spreadsheet."""
    return f"https://docs.google.com/spreadsheets/d/{_GOOGLE_SPREADSHEET_ID}"


def _index_sheet() -> gspread.Worksheet:
    """Get the index sheet containing the URL mappings.

    Returns the worksheet specified by DIRECTORY_SHEET_NAME environment variable,
    or the first sheet if not specified.
    """
    return (
        _client.worksheet(_DIRECTORY_SHEET_NAME)
        if _DIRECTORY_SHEET_NAME
        else _client.sheet1
    )


def find(path: str) -> list[str]:
    """Find all matching URLs for the given path in the index sheet.

    Searches column 1 of the sheet for cells matching the given path, then returns
    the corresponding URLs from column 2.

    The spreadsheet format should be:
    - Column 1: Short keys/identifiers
    - Column 2: Full URLs

    Args:
        path: The search key to look up in column 1

    Returns:
        A list of matching URLs from column 2. Empty list if no matches found.
        Filters out any None or empty values.

    Example:
        If the sheet contains:
        | docs | https://example.com/docs |
        | docs | https://example.org/docs |

        Then find("docs") returns:
        ["https://example.com/docs", "https://example.org/docs"]
    """
    sheet = _index_sheet()
    rows = [cell.row for cell in sheet.findall(path, in_column=1)]
    cells = [sheet.cell(row, 2) for row in rows]
    results = [cell.value for cell in cells if cell]
    return [r for r in results if r]

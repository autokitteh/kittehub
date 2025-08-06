"""walkthrough on how to get notifications a spreadsheet is edited."""


def filter_spreadsheet_event(event):
    """Filter events to only those related to spreadsheet changes."""
    print(event)
    file_type = event.data.get("file", {}).get("mime_type")
    if file_type != "application/vnd.google-apps.spreadsheet":
        return
    on_spreadsheet_change(event)


def on_spreadsheet_change(event):
    """Handle the event when a spreadsheet is edited."""
    file_id = event.data.get("file", {}).get("id")
    print(f"spread sheet with the ID ({file_id}) ")
    print("was edited")

"""walkthrough on how to get notifications a spreadsheet is edited."""


def on_spreadsheet_change(event):
    """Handle the event when a spreadsheet is edited."""
    file_id = event.data.get("file", {}).get("id")
    print(f"spreadsheet with the ID ({file_id}) ")
    print("was edited")

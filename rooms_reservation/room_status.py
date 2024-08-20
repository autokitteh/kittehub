
import helpers
from autokitteh.google import google_sheets_client
from autokitteh.google import google_calendar_client
from autokitteh.slack import slack_client
from datetime import UTC, datetime, timedelta

# Entry point for the /roomstatus slash command
def on_slack_roomstatus_slash_command(event):
    print(f"on_slack_roomstatus_slash_command()")
    
    slack = slack_client("slack_connection")

    #user_id = event.data['user_id'] 
    rooms = helpers.get_list_of_rooms() 
    channel_id = event.data['channel_id']      
    
    room_id = event.data['text']
    rooms = helpers.get_list_of_rooms() 
    if room_id not in rooms:
        slack.chat_postMessage(channel=channel_id, text=f"{room_id} not found in list of rooms")
        return

    gcal = google_calendar_client("calendar_conn").events()

    #TODO: change the time you would like to check for the room status
    now = datetime.now(UTC)
    in_5_hours = now + timedelta(hours=24)
    
    try:
        events_result = gcal.list(
            calendarId=room_id,
            timeMin=now.isoformat(),
            timeMax=in_5_hours.isoformat(),
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        events = events_result.get('items', [])

        msg = f'Events in {room_id}:'

        if not events:
            msg = msg + ' No upcoming events found.'
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            msg = msg + f"\n{start} - {event['summary']}"
        slack.chat_postMessage(channel=channel_id, text=msg)
    except Exception as e:
        slack.chat_postMessage(channel_id, f"{e}")
        print(f'Error: {e}')

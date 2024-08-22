# Room Reservarion System

In our organization, we manage meeting rooms as resources in Google Calendar:

- Each meeting room is represented by an email account
- To reserve a room for a meeting, users can add the room to the meeting invite

While users can reserve rooms directly from the calendar, we wanted to add a
Slack interface to make it even quicker to reserve a room for an immediate
meeting within the next half hour.

We configured three Slash commands in Slack:

- `/whatsfree` - Retrieves a list of free rooms for the next hour.
- `/roomstatus <room name>` - Provides the status of a specific room for the next hour.
- `/createmeeting <room name> <message>` - Reserves a specified room and leaves a message. (You can extend this workflow to add participants, set the time, etc.)

## Configuration

Each meeting room is represented by an email account.

The list of available meeting rooms is stored in a Google Sheet, which looks like this:


|-------------------|
| room1@example.com |
| room2@example.com |
| room3@example.com |

## AutoKitteh Integrations

Google Calendar, Google Sheets, Slack

## Implementation Languages

🐍 Python

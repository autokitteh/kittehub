# Jira to Google Calendar Workflow

This project automates the process of creating Google Calendar events based on Jira issue creation. When a new Jira issue is created, the workflow automatically generates a Google Calendar event with a deadline to ensure that the required tasks are completed on time.

## Benefits

- **Simplicity**: In a few lines of code, you have a functional workflow that is authenticated and integrated, allowing two applications to communicate with each other.
- **Flexibility**: Use this as a starting point. Add integrations or change the trigger. It's open source and free, so there are no limits to what you can do.

## How It Works

1. **Trigger**: The workflow is triggered by the creation of a new Jira issue.
2. **Create Calendar Event**: The program creates a Google Calendar event based on the Jira issue details, including the due date and description.
3. **Notify**: The event is created in the Google Calendar, and attendees are notified.

## Installation and Usage 

- [Install AutoKitteh](https://docs.autokitteh.com/get_started/install)

### Configure integrations

> [!IMPORTANT]
> The `autokitteh.yaml` file includes environment variables for the Jira and Google Calendar connections that need to be configured.

Ensure you have set up the required integrations:

- [Atlassian Jira](https://docs.autokitteh.com/integrations/atlassian)
- [Google Calendar](https://docs.autokitteh.com/integrations/google)

### Clone the Repository

```shell
git clone https://github.com/autokitteh/kittehub.git
cd kittehub/jira_google_calendar/deadline_to_event
```

Alternatively, you can copy the individual files in this directory.

### Run the AutoKitteh Server

Simply run this command:

```shell
ak up --mode dev
```

### Apply Manifest and Deploy Project

1. Navigate to the `deadline_to_event` directory:

```shell
cd deadline_to_event
```

2. Apply manifest and deploy the project by running the following command:

```shell
ak deploy --manifest autokitteh.yaml
```

The output of this command will be important for initializing connections in the following step if you're using the CLI.

For example, for each configured connection, you will see a line that looks similar to the one below:

```shell
[exec] create_connection "deadline_to_event/google_calendar_connection": con_01j36p9gj6e2nt87p9vap6rbmz created
```

`con_01j36p9gj6e2nt87p9vap6rbmz` is the connection ID.

### Initiliaze Connections

Using the connection IDs from the previous step, run these commands:

```shell
ak connection init my_jira <connection ID>
ak connection init my_google_calendar <connection ID>
```

### Trigger the Workflow

The workflow is triggered by the creation of a new Jira issue, which prompts the creation of a Google Calendar event according to the issue's details.

## Known Limitations

- Attendees are hard-coded and arbitrary.
- Error handling is not implemented for demo purposes. For example, if the Jira issue is missing any of the required fields (e.g., `description`, `duedate`), the program will not fail gracefully.

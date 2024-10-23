
# Google Calendar to Asana Task Creation Workflow

This project creates Asana tasks based on Google Calendar events.

## How It Works

1. The workflow is triggered by Google Calendar event creation for a specific calendar.

2. The workflow extracts the event details (title, description, etc.) and constructs an Asana task in a predefined Asana project.

3. The task is created with all necessary information from the calendar event, such as summary, due date and description.

> [!TIP]
> This workflow can be easily expanded by either pulling additional data from the Google Calendar event or adding fields to the Asana task.

## API Documentation

Asana:

- https://docs.autokitteh.com/integrations/asana

Google Calendar:

- https://docs.autokitteh.com/integrations/google/calendar

## Setup Instructions

1. Install and start a
   [self-hosted AutoKitteh server](https://docs.autokitteh.com/get_started/quickstart),
   or use AutoKitteh Cloud.

2.	Mandatory for self-hosted servers (preconfigured in AutoKitteh Cloud):

   - [Enable Google connections to use OAuth 2.0](https://docs.autokitteh.com/integrations/google/config)
   - [Enable Asana connections](https://docs.autokitteh.com/integrations/asana/connection)

3. Run this command to clone the Kittehub repository, which contains this
   project:

   ```shell
   git clone https://github.com/autokitteh/kittehub.git
   ```

4. Set the `ASANA_PROJECT_GID` variable in this project's
   [autokitteh.yaml](./autokitteh.yaml) manifest file.

   >[!TIP]
   > You can find the GID in the URL of the Asana project. It is the part after `/0/`. For example, in `https://app.asana.com/0/your_project_gid/list`, `your_project_gid`.

5. Run this command to deploy this project's manifest file:

   ```shell
   ak deploy --manifest kittehub/google_cal_to_asana/autokitteh.yaml
   ```

6. Initialize this project's connections:

   - Asana: with a PAT (Personal Access Token)
   - Google Calendar: with OAuth 2.0 or a service account's JSON key

> [!TIP]
> The exact CLI commands to do so (`ak connection init ...`) will appear in
> the output of the `ak deploy` command from step 5 when you create the
> project on the server, i.e. when you run that command for the first time.

> [!IMPORTANT]
> Specify the ID of a calendar that you own, to receive notifications about new events.

## Usage Instructions

1. Create an event in the Google Calendar that you specified in step 6 above.

2. See the Asana task which was auto-created in the Asana project that you
   specified in the [autokitteh.yaml](./autokitteh.yaml) manifest file.

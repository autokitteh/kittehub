# JIRA Assignee From Google Calendar Workflow 

This project automates the process of assigning Jira issues based on a shared Google Calendar. The workflow checks the current on-call person from the Google Calendar and assigns newly created Jira issues to them.

## Benefits

- **Focus on what matters**: Write code that focuses on the desired outcome, not the underlying infrastructure.
- **Flexibility**: Implement your own authorization flow or use the one that works out of the box.
- **Extensibility**: Easily add additional steps or integrations.

## How It Works

1. **Trigger**: A new Jira issue in the designated Jira project (specified in [`autokitteh.yaml`](./autokitteh.yaml))
2. **Check Calendar**: The program checks the shared Google Calendar to identify the current on-call person.
3. **Assign Issue**: The program assigns the newly created Jira issue to the current on-call person.

## Installation and Usage 

- [Install AutoKitteh](https://docs.autokitteh.com/get_started/install)

### Configure integrations

Ensure you have set up the required integrations. The `autokitteh.yaml` file includes environment variables for the Google Calendar and Jira connections that need to be configured.

- [Configure Atlassian integration](https://docs.autokitteh.com/config/integrations/atlassian)
- [Configure Google integration](https://docs.autokitteh.com/config/integrations/google)

### Clone the Repository

```shell
git clone https://github.com/autokitteh/kittehub.git
cd kittehub/assignee_from_schedule
```

Alternatively, you can copy the individual files in this directory.

### Run the AutoKitteh Server

Simply run this command:

```shell
ak up --mode dev
```

### Apply Manifest and Deploy Project

1. Navigate to the `assignee_from_schedule` directory:

```shell
cd assignee_from_schedule
```

2. Apply manifest and deploy the project by running the following command:

```shell
ak deploy --manifest autokitteh.yaml
```

The output of this command will be important for initializing connections in the following step if you're using the CLI.

For example, for each configured connection, you will see a line that looks similar to the one below:

```shell
[exec] create_connection "assignee_from_schedule/jira_connection": con_01j36p9gj6e2nt87p9vap6rbmz created   
```

`con_01j36p9gj6e2nt87p9vap6rbmz` is the connection ID.

### Initiliaze Connections

Using the connection IDs from the previous step, run these commands:

```shell
ak connection init jira_connection <connection ID>
ak connection init google_calendar_connection <connection ID>
```

### Trigger the Workflow

Once deployed, the workflow is triggered by the creation of a new Jira issue, which prompts the assignment to the current on-call person according to the shared Google Calendar.

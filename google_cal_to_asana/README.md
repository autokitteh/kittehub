
# Google Calendar to Asana Task Creation Workflow

This project automates the process of creating a new Asana task when a new event is created in Google Calendar. It listens for Google Calendar event creation and automatically creates a corresponding task in an Asana project.

## Benefits

- **Integration with Asana API:** Demonstrates how to integrate AutoKitteh with the Asana API for seamless task management.
- **Ease of Use:** Uses AutoKitteh's `asana_client` for handling authentication, making the integration secure and simple.


## Installation and Usage

1. [Install AutoKitteh](https://docs.autokitteh.com/get_started/install)
   
### Configure Integrations

- [Asana](https://docs.autokitteh.com/integrations/asana/connection)
- [Google Calendar](https://docs.autokitteh.com/integrations/google/config)

### Clone the Repository

```shell
git clone https://github.com/autokitteh/kittehub.git
cd kittehub/google_calendar_asana
```

Alternatively, you can copy the individual files in this directory.

### Run the AutoKitteh Server

Simply run this command:

```shell
ak up --mode dev
```

### Apply Manifest and Deploy Project

1. Navigate to the `google_calendar_asana` directory:

    ```shell
    cd google_cal_to_asana
    ```

2. Apply the manifest and deploy the project by running the following command:

    ```shell
    ak deploy --manifest autokitteh.yaml
    ```
   
   The output of this command will be important for initializing connections in the following step if you're using the CLI.

   For example, for each configured connection, you will see a line that looks similar to the one below:

    ```shell
    [exec] create_connection "google_calendar_asana/asana_conn": con_01j36p9gj6e2nt87p9vap6rbmz created
    ```

   `con_01j36p9gj6e2nt87p9vap6rbmz` is the connection ID.

### Initialize Connections

> [!IMPORTANT] 
> `asana_conn` needs to be initialized using the connection ID from the previous step.

Using the connection ID from the previous step, run this command:

```shell
ak connection init asana_conn <connection ID>
```

### Trigger the Workflow

The workflow is triggered when a new event is created in Google Calendar, automatically generating a corresponding task in Asana.


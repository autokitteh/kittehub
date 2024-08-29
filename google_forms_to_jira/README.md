
# Google Forms to Jira Workflow

This project automates the process of creating Jira issues based on new responses to a Google Form. The workflow periodically polls a Google Form for new responses and creates a Jira issue for each new response.

## Benefits

- **Automated Issue Creation**: Automatically creates Jira issues for each new Google Form response.
- **Seamless Integration**: Integrates Google Forms and Jira without additional manual steps.

## How It Works

1. **Trigger**: The workflow is triggered by an HTTP GET request.
2. **Poll Forms**: The program polls the specified Google Form for new responses.
3. **Create Jira Issue**: For each new response, the program creates a Jira issue with the response data.

## Installation and Usage 

- [Install AutoKitteh](https://docs.autokitteh.com/get_started/install)

### Configure integrations

> [!IMPORTANT]
> The `autokitteh.yaml` file includes environment variables for the Google Forms and Jira connections that need to be configured.

Ensure you have set up the required integrations: 

- [Atlassian Jira](https://docs.autokitteh.com/integrations/atlassian)
- [Google Forms](https://docs.autokitteh.com/integrations/google)

### Clone the Repository

```shell
git clone https://github.com/autokitteh/kittehub.git
cd kittehub/google_forms_to_jira
```
Alternatively, you can copy the individual files in this directory.

### Run the AutoKitteh Server

Simply run this command:

```shell
ak up --mode dev
```

### Apply Manifest and Deploy Project

1. Navigate to the `google_forms_to_jira` directory:

   ```shell
   cd google_forms_to_jira
   ```

2. Apply manifest and deploy the project by running the following command:

   ```shell
   ak deploy --manifest autokitteh.yaml
   ```

   The output of this command will be important for initializing connections in the following step if you're using the CLI.

   For example, for each configured connection, you will see a line that looks similar to the one below:

   ```shell
   [exec] create_connection "google_forms_to_jira/jira_connection": con_01j36p9gj6e2nt87p9vap6rbmz created
   ```

   `con_01j36p9gj6e2nt87p9vap6rbmz` is the connection ID.

### Initiliaze Connections

> [!NOTE] 
> `my_http` does not need to initialized

Using the connection IDs from the previous step, run these commands:

```shell
ak connection init jira_connection <connection ID>
ak connection init google_forms_connection <connection ID>
```

### Trigger the Workflow

The workflow is triggered by an HTTP GET request to http://localhost:9980/http/google_forms_to_jira/, which starts the polling process for new Google Form responses.

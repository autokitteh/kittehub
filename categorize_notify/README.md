# Email Categorization and Notification Workflow
This project automates the process of categorizing incoming emails and notifying relevant Slack channels by integrating Gmail, ChatGPT, and Slack. It is not meant to be a 100% complete project, but rather a solid starting point.

## Benefits
- **Ease of Use:** Demonstrates how easy it is to connect multiple integrations into a cohesive workflow.
- **Low Complexity:** The workflow is implemented with a minimal amount of code.
- **Free and Open Source:** Available for use or modification to fit specific use cases. 

## How It Works
- **Detect New Email**: The program monitors the Gmail inbox for new emails using the Gmail API.
- **Categorize Email**: ChatGPT analyzes the email content and categorizes it into predefined categories.
- **Send Slack Notification**: The program sends the categorized email content to the corresponding Slack channel using the Slack API.
- **Label Email**: Adds a label to the processed email in Gmail for tracking.

For more details, refer to [this blog post](https://autokitteh.com/technical-blog/from-inbox-to-slack-automating-email-categorization-and-notifications-with-ai/).

## Installation Instructions
If you're using VS Code, make sure to [install the AutoKitteh extension](https://docs.autokitteh.com/get_started/client/vscode/install) before proceeding.
### Mac 
To install on Mac, run the following command:
```shell
brew install autokitteh/tap/autokitteh
``` 
### Linux
For Linux installation instructions, click [here](https://docs.autokitteh.com/get_started/install?os=linux).

### Windows
For Windows installation instructions, click [here](https://docs.autokitteh.com/get_started/install?os=windows).

### Clone the Repository
```shell
git clone https://github.com/autokitteh/kittehub.git
cd kittehub/categorize_notify
```
Alternatively, you can the copy individual files in this directory.

### Run the AutoKitteh Server
Simply run this command:

```shell
ak up --mode dev
```

### Apply Manifest and Deploy Project

#### CLI
1. Navigate to the `categorize_notify` directory:

   ```shell
   cd categorize_notify
   ```

2. Apply manifest and deploy project by running the following command:

   ```shell
   ak deploy --manifest autokitteh-python.yaml --file program.py
    ```
    The output of this command will be important for initializing connections in the following step if you're using the CLI.

    For example, for each configured connection, you will see a line that looks similar to the one below:

    ```shell
    [exec] create_connection "categorize_notify/my_chatgpt": con_01j36p9gj6e2nt87p9vap6rbmz created
    ```

    `con_01j36p9gj6e2nt87p9vap6rbmz` is the connection ID.    
#### VS Code
1. Open the project's YAML manifest file
2. In the VS Code command palette, run: `AutoKitteh: Apply Manifest`
3. Open AutoKitteh VS Code extension
4. To the right of the project title, select `Run Project`

### Initiliaze Connections
#### CLI
>💡 **Note**: `my_http` does not need to initialized

Run these commands:
<!-- TODO: Change the commands below to working commands -->
```shell
ak connection init my_chatgpt <connection ID>
ak connection init my_gmail <connection ID>
ak connection init my_slack <connection ID>
```
Alternatively, you can initialize connections using VS Code.

#### VS Code
1. Open the AutoKitteh extension
2. Select `categorize_notify`
3. Click on connections
![](../../static/img/connect_init.png)
4. Click on the cog wheel next to `my_chatgpt`, `my_gmail` and `my_slack` connections to be redirected to their respective initialization page
![](../../static/img/connect_init2.png)


### Trigger the Workflow
Run this command:

```shell
curl -v "http://localhost:9980/http/categorize_notify/"
```
## Known Limitations
- **ChatGPT**: the prompt for this workflow works for simple cases. It may have mixed results for emails that lack detail or have nothing to do with the channels provided.
- **E-mail polling**: the polling mechanism is basic and does not cover edge cases.

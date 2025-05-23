# Basic Discord Bot with AutoKitteh

[![Start with AutoKitteh](https://autokitteh.com/assets/autokitteh-badge.svg)](https://app.autokitteh.cloud/template?name=samples/discord/discord_client)

This project demonstrates how to use AutoKitteh's Discord integration to create a basic Discord bot that performs simple operations. The bot connects to Discord, waits until it is ready, and then sends a "Meow!" message to a specified channel. This example serves as a foundational guide for integrating AutoKitteh's Discord capabilities into your own projects.

## Benefits

- **Simple Integration:** Quickly set up a Discord bot using AutoKitteh's Discord integration.
- **Event Handling:** Listens for the `on_ready` event and can be extended to handle more events.
- **Modular Design:** Easily extend or modify the program to suit specific needs, such as adding commands or integrating with external services.
- **Open Source:** Feel free to modify and use this program in your own projects.

## How It Works

- **AutoKitteh Discord Integration:** Utilizes AutoKitteh's Discord integration to create a Discord client.
- **Event Handling:** The bot listens for the `on_ready` event, triggered upon successful connection to Discord.
- **Sending a Message:** Upon the `on_ready` event, the bot sends a "Meow!" message to a specified channel.
- **Error Handling:** Handles exceptions related to permissions and HTTP issues when sending messages.

## Installation and Usage 

> [!NOTE]
> This sample currently works only on the local version of AutoKitteh and is not compatible with the cloud version.

1. **Clone the Repository:**

   ```shell
   git clone https://github.com/autokitteh/kittehub.git
   cd kittehub/discord_basic_bot
   ```

2. **Install AutoKitteh:**

   Follow the installation guide for AutoKitteh:

   [AutoKitteh Installation](https://docs.autokitteh.com/get_started/install)

3. **Configure Discord Integration:**

   Set up your Discord bot and connection using the documentation:

   [Discord Integration Guide](https://docs.autokitteh.com/integrations/discord/connection)


4. **Run the AutoKitteh Server:**

   Start the AutoKitteh server in development mode:

   ```shell
   ak up --mode dev
   ```

5. **Initialize the Connection:**

   Using the connection ID from the previous step, initialize the Discord connection:

   ```shell
   ak connection init discord_conn <connection ID>
   ```

6. **Deploy the Project:**

   Apply the manifest and deploy the project:

   ```shell
   ak deploy --manifest autokitteh.yaml
   ```


7. Look for the following lines in the output of the `ak deploy` command, and
   copy the URL paths for later:

   ```
   [!!!!] trigger "..." created, webhook path is "/webhooks/..."
   ```

> [!TIP]
> If you don't see the output of `ak deploy` anymore, you can run this
> command instead, and use the webhook slugs from their outputs:
>
> ```shell
> ak trigger get start_event_loop --project discord_client_sample -J
> ```

8. **Start the Bot:**

   Trigger the workflow:

   ```shell
   curl -v "http://localhost:9980/webhooks/<webhook slug>"
   ```

9. **Bot Operation:**

   The bot will connect to Discord and send a "Meow!" message to the specified channel upon startup.

## Notes

- **Event Loop:** The bot uses an event loop to maintain the connection to Discord and listen for events.

> [!WARNING]
> If you don't explicitly close the client connection with `client.close()`, this will result in duplicate messages being sent and other unpredictable behavior.

- **Extensibility:** You can add more event handlers to the bot by using the `@client.event` decorator. 
- **Permissions:** Ensure the bot has the necessary permissions to send messages in the specified channel.

# Discord Events

[![Start with AutoKitteh](https://autokitteh.com/assets/autokitteh-badge.svg)](https://app.autokitteh.cloud/template?template-name=samples/discord/events)

This project demonstrates how to utilize AutoKitteh's event system for Discord, offering a simpler alternative to the [discord.py library](../discord_client/) when working with supported [events](https://docs.autokitteh.com/integrations/discord/events). The program listens for message-related events (message creation, update, and deletion) in Discord and logs the corresponding information. This example serves as a foundational guide for integrating AutoKitteh's Discord event handling with other services.

## Benefits

- **Simple Integration:** This workflow is designed to easily connect Discord to custom logging or processing systems.
- **Modular Design:** You can extend or modify this program to suit your specific needs, such as adding more event types or integrating with external APIs.
- **Open Source:** Feel free to modify and use this program in your own projects.

## How It Works

- **Message Events:** The program listens for three types of message events in Discord:
  - `Message Create`: Captures when a message is sent and logs the username and message content.
  - `Message Update`: Logs when a message is updated.
  - `Message Delete`: Logs when a message is deleted.

## Installation and Usage 

> [!NOTE]
> This sample currently works only on the local version of AutoKitteh and is not compatible with the cloud version.

1. Clone the Repository:
   
   ```bash
   git clone https://github.com/autokitteh/kittehub.git
   cd kittehub/discord_message_logger
   ```

2. Install AutoKitteh:

   Follow the installation guide for AutoKitteh:
   [AutoKitteh Installation](https://docs.autokitteh.com/get_started/install)

3. Configure Discord Integration:

   Set up your Discord bot and connection using the documentation:
   [Discord Integration Guide](https://docs.autokitteh.com/integrations/discord/connection)

4. Run the AutoKitteh Server:
   
   Run the following command to start the server:
   ```bash
   ak up --mode dev
   ```

5. Deploy the Project:

   Apply the manifest and deploy the project:
   ```bash
   ak deploy --manifest autokitteh.yaml
   ```

   This command will output a connection ID for your Discord integration.

6. Initialize the Connection:

   Using the connection ID from the previous step, initialize the Discord connection:
   ```bash
   ak connection init discord_conn <connection ID>
   ```

7. Start Logging Discord Messages:

   The workflow will be triggered automatically when a message-related event occurs in Discord.

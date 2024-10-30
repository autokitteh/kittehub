
# Quickstart

Basic tutorial workflow.

## Running the workflow using AutoKitteh UI

1. Go to the "Assets" page from the top left menu and click "Deploy" in the top right corner.

   > [!NOTE]
   > You should see the message: "Success. Project deployment completed successfully." You can also verify this by navigating to the "Deployments" page and checking for a new deployment.

2. In the "Assets" page, select the "TRIGGERS" tab.

   > [!NOTE]
   > A table with one pre-populated row should appear, with columns: "Name, Source, Call, and Actions." The row should show a trigger named "http_request."

   In the "Actions" column, there are two icons: modify (left) and delete (right). Click the left icon to modify the trigger.

3. Copy the "Webhook URL" from the last input field (the one with the copy icon).

4. Run the following command with the copied URL:

   ```bash
   curl -i "https://api.autokitteh.cloud/webhooks/..."
   ```

5. Go to "Sessions" (top left menu) to check if a session was created. You should see a session with a `COMPLETED` status. Click the session to review the logs and confirm the workflow ran as expected.

6. Run this command to trigger the workflow again, with an additional query parameter (iterations set to 50):

   ```bash
   curl -i "https://api.autokitteh.cloud/webhooks/..." --url-query iterations=50
   ```

   > [!NOTE]
   > This command runs the workflow in a loop, instead of printing a single message:
   > ```python
   > for i in range(iterations):
   >    print(f"Loop iteration: {i + 1} of {iterations}")
   >    time.sleep(FIVE_SECONDS)
   > ```

7. Return to "Sessions." The new session's status will be `RUNNING`. Select the latest session to view the following print messages:

   ```
   [2024-30-10 14:03:44]: Loop iteration: 3 of 50
   [2024-30-10 14:03:39]: Loop iteration: 2 of 50
   [2024-30-10 14:03:33]: Loop iteration: 1 of 50
   [2024-30-10 14:03:33]: Received GET request
   ```

## Self-Hosted Setup and Usage Instructions

For more details, visit the [Quickstart Guide](https://docs.autokitteh.com/get_started/quickstart).

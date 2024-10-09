
# GitHub Workflow Orchestration

This AutoKitteh project automates the process of handling GitHub workflows that interact across multiple repositories, 
triggering actions in specific repositories based on the completion of workflows in other repositories.

## Benefits

- **Automated Workflow Management**: Simplifies managing dependencies between multiple GitHub repositories.
- **Scalable Integration**: Easily handles complex trigger scenarios like fan-in and fan-out.
- **Minimized Manual Effort**: Reduces the need for manual intervention by automating cross-repo workflow execution.

## Additional Documentation

- [Python client API](https://pygithub.readthedocs.io/en/latest/index.html)
- [`subscribe`/`next_event`](https://docs.autokitteh.com/glossary/event/)

## Setup Instructions

1. Install and start a 
   [self-hosted AutoKitteh server](https://docs.autokitteh.com/get_started/quickstart), 
   or use AutoKitteh Cloud.

2. [Configure your GitHub integration](https://docs.autokitteh.com/integrations/github).

3. Run these commands to deploy this project's manifest file:

   ```shell
   git clone https://github.com/autokitteh/kittehub.git
   ak deploy --manifest kittehub/github_actions/autokitteh.yaml
   ```

4. Look for the following lines in the output of the `ak deploy` command, and 
   copy the URL paths for later:

   ```
   [!!!!] trigger "..." created, webhook path is "/webhooks/..."
   ```

> [!TIP]
> If you don't see the output of `ak deploy` anymore, you can run these 
> commands instead, and use the webhook slugs from their outputs:
>
> ```shell
> ak trigger get cross_repo --project github_actions -J
> ak trigger get fan_out --project github_actions -J
> ak trigger get or_trigger --project github_actions -J
> ak trigger get fan_in --project github_actions -J
> ```

## Usage Instructions

1. Run these commands to start sessions for the Cross-repo trigger 
   (use the **1st** URL path from step 4 above):

   ```shell
   curl -i "http://localhost:9980/webhooks/<webhook-slug>/cross-repo"
   ```

2. Run this command to initiate the Fan-out trigger 
   (use the **2nd** URL path from step 3 above):

   ```shell
   curl -i "http://localhost:9980/webhooks/<webhook-slug>/fan-out"
   ```

3. Run this command for the OR trigger 
   (use the **3rd** URL path from step 3 above):

   ```shell
   curl -i "http://localhost:9980/webhooks/<webhook-slug>/or-trigger"
   ```

4. Run this command for the Fan-in trigger 
   (use the **4th** URL path from step 3 above):

   ```shell
   curl -i "http://localhost:9980/webhooks/<webhook-slug>/fan-in"
   ```

5. Check out the resulting session logs in the AutoKitteh server for each of 
   the steps above to verify the triggers were executed as expected.

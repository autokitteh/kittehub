# GitHub Copilot Registration Pruning

This automation searches daily for all users in a GitHub organization that are actively using Copilot.
If Copilot was not used in a preceding period, it automatically unregisters them, and then notifies them.
Users can then optionally ask for their subscription to be reinstated.

## Slack Usage

- `/ak prune-idle-copilot-seats` invokes the automation immediately.
- `/ak find-idle-copilot-seats` displays the potentially idle seats.

> [!WARNING]
> This example currently works only with a [Personal Access Token](https://docs.autokitteh.com/integrations/github/connection/#personal-access-token-pat), specifically a [classic token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-personal-access-token-classic).

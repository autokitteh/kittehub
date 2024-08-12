# GitHub Copilot Registration Pruning

This automation searches daily for all users in a GitHub organization that are actively using Copilot.
If Copilot was not used in a preceding period, it automatically unregisters them, and then notifies them.
Users can then optionally ask for their subscription to be reinstated.

## Slack Usage

- `/ak prune-idle-copilot-seats` invokes the automation immediately.
- `/ak find-idle-copilot-seats` displays the potentially idle seats.

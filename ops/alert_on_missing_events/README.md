---
title: Alert on missing events
description: Send alerts when AutoKitteh doesn't receive certain events in time
integrations: ["Jira", "Slack"]
categories: ["Ops"]
---

# Alert on Missing Events

Send alerts when AutoKitteh doesn't receive certain events in time.

This is a detection tool for incidents due to missing updates from
monitored services. Possible root-causes for example:

- The monitored service is down / local network outage
- The integration's callback URL has been modified
- The connection's event watches have expired

While an incident is ongoing, the workflow continues to wait for the desired
events, and resends reminder alerts at a shorter interval.

## Configuration and Deployment

### Cloud Usage

1. Import/upload the project
2. Initialize your connections

> [!TIP] The default monitored service is Jira. If you want to monitor a
> different service:
>
> 1. Delete the `monitored_service_conn` connection
> 2. Recreate a new connection with the same name, and select the desired
>    integration
> 3. Delete the `monitor_trigger` trigger
> 4. Recreate a new trigger, select the new `monitored_service_conn`
>    connection from step 2, and configure it

3. Edit the trigger

   - Specifically, select an `Event Type` and/or set the CEL expression in
     the `Filter` field to match only the events you want to monitor

4. Set/modify these project variables:

   - `EVENT_FILTER`: must be identical/equivalent to the `Event Type` and/or
     `Filter` fields of the trigger in step 2!
   - `EVENT_DESCRIPTION`: human-readable description of the events that should
     be received, displayed in alert messages
   - `TIMEOUT_HOURS`: it's OK not to receive events up to this amount of time
     (default = `24` hours)
   - `PING_HOURS`: while an incident is ongoing, re-check at a shorter interval
     (default = `1` hour)
   - `SLACK_CHANNEL`: send incident alerts to this Slack channel name/ID
     (default = `autokitteh-alerts`)

5. Deploy the project

### Self-Hosted Usage

Follow [these detailed instructions](https://docs.autokitteh.com/get_started/deployment)
to deploy the project on a self-hosted server.

Also follow the instructions in the [Cloud Usage](#cloud-usage) section above.

### Advanced Usage

You can add this project's configuration and code to existing projects, or run
it in parallel to them. Either way, all matching triggers in AutoKitteh will
receive all the events that match the specified criteria.

You can also duplicate or extend this mechanism to handle multiple events and
connections in a single project. AutoKitteh sessions are isolated from each
other.

---
title: Alert on missing events
description: Send alerts when AutoKitteh doesn't receive certain events in time
integrations: ["Slack"]
categories: ["Ops"]
---

# Alert on Missing Events

Send alerts when AutoKitteh doesn't receive certain events in time. This
detects incidents due to missing updates from monitored services.

Possible causes for example:

- The monitored service is down / local network outage
- The integration's callback URL has been modified
- The connection's event watches have expired

While an incident is ongoing, the workflow continues to wait for the desired
events, and resends reminder alerts at a shorter interval.

---

You can add this project's configuration and code to existing projects, or run
it in parallel to them. Either way, all matching triggers in AutoKitteh will
receive each conformant event.

You can also duplicate or extend this mechanism to handle multiple events and
connections in a single project. AutoKitteh sessions are isolated from each
other.

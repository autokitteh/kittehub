---
title: Incident management automation
description: Slack/Zoom/Height Incident Automation
integrations: ["slack", "zoom", "height"]
categories: ["Reliability"]
---

# Incident Management Automation

An incident can be created by mentioning the Slack bot like so:

```
@ak incident title
```

This will create a Zoom meeting, a Height ticket, and a Slack channel for the incident.
In the Slack channel, incident is resolved by writing "!resolve why this was resolved". A note can be added
to the ticket with "!note something to write home about".

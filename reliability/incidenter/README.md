---
title: Incident management automation
description: Connect separate systems to have seamless incident management
integrations: ["slack", "zoom", "height"]
categories: ["Reliability"]
---

# Incident Management Automation

[![Start with AutoKitteh](https://autokitteh.com/assets/autokitteh-badge.svg)](https://app.autokitteh.cloud/template?name=reliability/incidenter)

An incident can be declared by mentioning the Slack bot like so:

```
@ak incident title
```

This will create a dedicated Slack channel, a dedicated Zoom meeting, and a tracking ticket in Height.

Notes can be added to the Height ticket by writing `"!note <text>"` in the created Slack channel.

The incident can be resolved by writing `"!resolve <reason text>"` in the created Slack channel.

---
title: Source control compliance controls
description: Audit compliance controls related to source control systems
integrations: ["github", "sheets"]
categories: ["Compliance"]
---

# Source Control Compliance Controls

Audit compliance controls related to source control systems (GitHub):

- All commits have authorized and verified authors
- All code changes are reviewed:
  - No commits directly to the main branch without a PR
  - PRs are approved by another developer before merging
- No automated test failures for merged PRs

Violations are tracked in a Google Sheet for auditing purposes.

In addition, we use AI to...

Lastly, this project also reacts in real time to...

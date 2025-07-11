---
title: GitHub workflow orchestration
description: Orchestrate GitHub workflows using advanced scenarios across multiple repositories
integrations: ["github"]
categories: ["DevOps"]
tags: ["webhook_handling", "parallel_processing", "monitoring", "notifications"]
---

# GitHub Workflow Orchestration

[![Start with AutoKitteh](https://autokitteh.com/assets/autokitteh-badge.svg)](https://app.autokitteh.cloud/template?name=devops/github_workflows)

Orchestrate GitHub workflows with advanced scenarios across multiple repositories:

- Cross-repo (A &rarr; B)
- Fan-out (A &rarr; B and C in parallel)
- Any-to-one reduction (first of A or B &rarr; C)
- All-to-one fan-in (A and B &rarr; C)
- Long sequence (A &rarr; B &rarr; C &rarr; A &rarr; B &rarr; C)

> [!NOTE]
> GitHub cannot chain more than [4 workflows](https://docs.github.com/en/actions/writing-workflows/choosing-when-your-workflow-runs/events-that-trigger-workflows#workflow_run) automatically (when using `workflow_run` events), so the last scenario is useful even within a single repository.

## GitHub Prerequisites

This project requires 3 GitHub workflows that belong to different organizations and repositories. This demonstrates an important capability beyond GitHub's own workflow orchestration.

> [!TIP]
> For sake of setup simplicity, you may also configure this project to use 3 repositories belonging to a single owner, or even 3 separate workflows within the same repository.

For each workflow, you need to specify these details:

- Repository name (e.g. [`autokitteh/kittehub`](https://github.com/autokitteh/kittehub/))
- Workflow file path in that repository (e.g. [`.github/workflows/ci.yml`](https://github.com/autokitteh/kittehub/tree/main/.github/workflows/ci.yml))

> [!IMPORTANT]
> The workflow must be [triggered](https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions#on) by (at least) the [`workflow_dispatch`](https://docs.github.com/en/actions/writing-workflows/choosing-when-your-workflow-runs/events-that-trigger-workflows#workflow_dispatch) event.
>
> Example:
>
> ```yaml
> on: workflow_dispatch
> jobs:
>   job-name:
>     runs-on: ubuntu-latest
>     steps:
>       - run: echo "Do stuff"
> ```

## Cloud Usage

1. Initialize your GitHub connection
2. Copy all the webhook URLs from the "Triggers" tab (see the [instructions here](https://docs.autokitteh.com/get_started/deployment#webhook-urls))
3. Set all the project variables (based on the [GitHub Prerequisites](#github-prerequisites) section above):

   - `REPO_A`, `REPO_B`, `REPO_C`
   - `WORKFLOW_A`, `WORKFLOW_B`, `WORKFLOW_C`

4. Deploy the project

## Trigger Workflow

> [!IMPORTANT]
> Ensure the GitHub connection is properly initialized; otherwise the workflow will raise a `ConnectionInitError`.
>
> Also ensure all the project variables are configured correctly; otherwise the workflow may not work as expected.

Send HTTP GET requests to the webhook URLs from step 2 in the [Cloud Usage](#cloud-usage) section above:

```shell
curl -i "${WEBHOOK_URL}"
```

Check out the results in the GitHub repositories and in the AutoKitteh session logs.

> [!TIP]
> All workflows can also be triggered manually by clicking the "Run" button in the UI, and selecting desired entry-point function.

## Self-Hosted Deployment

Follow [these detailed instructions](https://docs.autokitteh.com/get_started/deployment) to deploy the project on a self-hosted server.

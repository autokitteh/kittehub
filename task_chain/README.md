# Task Chain

[![Start with AutoKitteh](https://autokitteh.com/assets/autokitteh-badge.svg)](https://app.autokitteh.cloud/template?template-name=task_chain)

This project runs a sequence of tasks with fault tolerance.

The workflow is resilient to errors in each step (with the ability to retry
each failing step on-demand via Slack), as well as server-side failures
(thanks to AutoKitteh's durable execution).

<img src="./images/slack1.png" width="366" height="210" alt="Slack screenshot 1">
<img src="./images/slack2.png" width="366" height="295" alt="Slack screenshot 2">

This directory contains three variants of this project:

1. **Single-workflow approach**: a single workflow runs all the tasks,
   including retry loops; it handles Slack interactions using runtime event
   subscriptions

   1. ["Basic" mode](./single_workflow/basic/) - an explicit specification of
      the transitions between steps, and each step is retried in its own loop

   2. ["Advanced" mode](./single_workflow/advanced/) - a single loop iterates
      over a global list of all the steps, and handles all the retries

```mermaid
flowchart LR
    slack{"`Slack
    Event`"}
    task1[Task 1]
    task2[Task 2]
    task3[Task 3]
    task4[Task 4]
    message{"`Retry/Abort
    Message`"}
    wend(("`Workflow
    End`"))

    subgraph Workflow 1
        direction LR
        slack -. Slash Command .-> task1 --> task2 --> task3
        task3 -- Success --> task4 -.-> wend
        task3 -- Error --> message
        message -- Retry --> task3
        message -. Abort .-> wend
    end
```

2. **[Event-driven approach](./event_driven/)**: a single workflow runs
   multiple tasks, except for retries, which branch into separate workflows

```mermaid
flowchart TB
    slack1{"`Slack
    Event`"}
    task1[Task 1]
    task2[Task 2]
    task3a[Task 3]
    error(("`Workflow
    Error`"))

    slack2{"`Slack
    Event`"}
    task3b[Task 3 Retry]
    task4[Task 4]
    success(("`Workflow
    Success`"))

    subgraph w1 [Workflow 1]
        direction LR
        slack1 -. Slash Command .-> task1 --> task2 --> task3a -.-> error
    end

    subgraph w2 [Workflow 2]
        direction LR
        slack2 -. Retry Button Clicked .-> task3b --> task4 -.-> success
    end

    w1 -. Retry/Abort Message .-> w2
```

# Task Chain

This project demonstrates running a sequence of tasks, in three ways.

1. **Single-workflow approach**: a single workflow runs all the tasks,
   including retry loops; it handles Slack interactions using runtime event
   subscriptions

   1. ["Basic" mode](./single_workflow/basic/) - an explicit specification of
      the transition between steps, and each step is retried in its own loop

   2. ["Advanced" mode](./single_workflow/advanced/) - a single loop iterating
      over a global list of all the steps, and handling all retries

2. **[Event-driven approach](./event_driven/)**: a single workflow runs
   multiple tasks, except for retries, which branch into separate workflows;
   see the following flowchart diagram:

```mermaid
flowchart LR
    slack1{"`Slack
    Event`"}
    slack2{"`Slack
    Event`"}
    task1[Task 1]
    task2[Task 2]
    task3a[Task 3]
    task3b[Task 3 Retry]
    task4[Task 4]
    error(("`Workflow
    Error`"))
    success(("`Workflow
    Success`"))
    subgraph Workflow 1
    slack1 -. Slash Command .-> task1 --> task2 --> task3a -.-> error
    end
    subgraph Workflow 2
    slack2 -. Retry Button Clicked .-> task3b --> task4 -.-> success
    end
    error -. Retry/Abort Message .-> slack2
```

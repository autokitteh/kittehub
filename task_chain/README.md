# Task Chain

This project demonstrates running a sequence of tasks, in several ways.

- Single-workflow approach:
  - A single workflow runs all the tasks, including retry loops; it handles
    Slack interactions using runtime event subscriptions
  - ["Basic" mode](./single_workflow/basic/) - ...
  - ["Advanced" mode](./single_workflow/advanced/) - ...
- [Event-driven approach](./event_driven/)
  - A single workflow runs all the tasks, except retries

```mermaid
flowchart LR
    slack{Slack event}
    task1[Task 1]
    task2[Task 2]
    task3a[Task 3]
    task3b[Task 3 retry]
    task4[Task 4]
    error((fa:fa-circle-xmark Workflow error))
    success((fa:fa-circle-check Workflow success))
    slack -. Slash command .-> task1
    slack -. Retry button clicked .-> task3b
    subgraph Workflow 1
    task1 --> task2 --> task3a -.-> error
    end
    subgraph Workflow 2
    task3b --> task4 -.-> success
    end
```

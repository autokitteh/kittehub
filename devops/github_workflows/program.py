"""Orchestrate GitHub workflows using advanced scenarios across repositories.

See the configuration and deployment instructions in the README.md file.
"""

import os

import autokitteh
from autokitteh.github import github_client
import github


# Indexes in the following lists, used throughout this module.
A = 0
B = 1
C = 2

# GitHub repositories (e.g. "autokitteh/kittehub").
REPOS = [
    os.getenv("REPO_A", ""),
    os.getenv("REPO_B", ""),
    os.getenv("REPO_C", ""),
]

# GitHub workflow file paths (e.g. ".github/workflows/ci.yml").
WORKFLOWS = [
    os.getenv("WORKFLOW_A", ""),
    os.getenv("WORKFLOW_B", ""),
    os.getenv("WORKFLOW_C", ""),
]

gh = github_client("github_conn")


def dispatch_workflow_manually(event: dict[str, str]) -> None:
    """Dispatch a workflow manually, for testing purposes.

    You may specify an optional index (default = 0 = workflow A).
    """
    _dispatch_workflow(int(event.get("index", A)))


def cross_repo(_) -> None:
    """Cross-repo demo (A --> B)."""
    sub = _subscribe_to_events(A)
    print("Waiting until workflow A completes")
    autokitteh.next_event(sub)
    print("Workflow A completed")
    _dispatch_workflow(B)


def fan_out(_) -> None:
    """Fan-out demo (A --> B and C in parallel)."""
    sub = _subscribe_to_events(A)
    print("Waiting until workflow A completes")
    autokitteh.next_event(sub)
    print("Workflow A completed")
    _dispatch_workflow(B)
    _dispatch_workflow(C)


def or_reduction(_) -> None:
    """Any-to-one reduction demo (first of A or B --> C)."""
    subs = [_subscribe_to_events(A), _subscribe_to_events(B)]
    print("Waiting until either workflow A or B complete (whichever comes first)")
    data = autokitteh.next_event(subs)
    print(f"Workflow completed: {data.repository.name}/{data.workflow.path}")
    _dispatch_workflow(C)


def fan_in(_) -> None:
    """All-to-one fan-in demo (A and B --> C)."""
    subs = [_subscribe_to_events(A), _subscribe_to_events(B)]

    # Wait until both workflows A and B complete.
    completed_workflows = set()
    while len(completed_workflows) < 2:
        data = autokitteh.next_event(subs)
        path = f"{data.repository.name}/{data.workflow.path}"
        print(f"Workflow completed: {path}")
        completed_workflows.add(path)

    _dispatch_workflow(C)


def long_sequence(_) -> None:
    """Long sequence demo (A --> B --> C --> A --> B --> C).

    Note: GitHub cannot chain more than 4 workflows (when using `workflow_run` events),
    so this AutoKitteh demo is useful even within a single repository. See details here:
    https://docs.github.com/en/actions/writing-workflows/choosing-when-your-workflow-runs/events-that-trigger-workflows#workflow_run
    """
    sub = _subscribe_to_events(A)
    print("Waiting until workflow A completes")
    autokitteh.next_event(sub)
    autokitteh.unsubscribe(sub)
    print("Workflow A completed")

    for wf in [B, C, A, B, C]:
        sub = _subscribe_to_events(wf)
        _dispatch_workflow(wf)
        print(f"Waiting until workflow {_index2char(wf)(wf)} completes")
        autokitteh.next_event(sub)
        autokitteh.unsubscribe(sub)
        print(f"Workflow {_index2char(wf)(wf)} completed")


def _subscribe_to_events(wf: int, conclusion: str = "success") -> str:
    """Intercept specific GitHub "workflow_run" events.

    API documentation:
    - https://docs.github.com/en/actions/writing-workflows/choosing-when-your-workflow-runs/events-that-trigger-workflows#workflow_run
    - https://docs.github.com/en/webhooks/webhook-events-and-payloads#workflow_run

    Args:
        wf: Workflow index (0-2).
        conclusion: Workflow completion result: "action_required",
            "cancelled", "failure", "neutral", "skipped", "stale",
            "success", "timed_out", "startup_failure", or None.

    Returns:
        AutoKitteh event subscription UUID.
    """
    conditions = [
        "event_type == 'workflow_run'",
        "data.action == 'completed'",
        f"data.workflow_run.conclusion == '{conclusion}'",
        f"data.repository.full_name == '{REPOS[wf]}'",
        f"data.workflow.path == '{WORKFLOWS[wf]}'",
    ]
    return autokitteh.subscribe("github_conn", " && ".join(conditions))


def _dispatch_workflow(wf: int, ref: str = "main", inputs: dict = None) -> None:
    """Start a specific GitHub workflow.

    API documentation:
    - https://docs.github.com/en/rest/actions/workflows#create-a-workflow-dispatch-event
    - https://docs.github.com/en/actions/writing-workflows/choosing-when-your-workflow-runs/events-that-trigger-workflows#workflow_dispatch

    Args:
        wf: Workflow index (0-2).
        ref: Git reference, should be the default branch (e.g. "main").
        inputs: Keys and values configured in the workflow file. The maximum
            number of properties is 10. Any default properties configured in
            the workflow file will be used when inputs are omitted.
    """
    repo = gh.get_repo(REPOS[wf])
    workflow = _get_workflow(repo, WORKFLOWS[wf])
    if workflow.create_dispatch(ref, inputs or {}):
        print(f"Workflow {_index2char(wf)(wf)} dispatched")
    else:
        print("Failed to create a 'workflow_dispatch' event")


def _get_workflow(repo: github.Repository, path: str) -> github.Workflow:
    """Return the GitHub workflow instance with the given file path."""
    for workflow in repo.get_workflows():
        if workflow.path == path:
            return workflow

    raise RuntimeError(f"Workflow file not found: {path}")


def _index2char(index: int) -> str:
    """Convert an index (0-2) to a workflow identifier (A-C)."""
    return chr(65 + index)

"""This program provides functions to handle GitHub workflows that interact across multiple repositories.
It defines triggers that automatically start workflows in specific repositories when workflows in other
repositories are completed.

This program supports several types of triggers:
1. Cross-repo trigger: Initiates a workflow in repository B when a workflow in repository A completes.
2. Fan-out trigger: Initiates workflows in repositories B and C upon the completion of a workflow in repository A.
3. OR trigger: Initiates a workflow in repository C if a workflow in either repository A or B completes.
4. Fan-in trigger: Initiates a workflow in repository C only when workflows in both repositories A and B complete.
"""

import os
import autokitteh
from autokitteh.github import github_client

REPO_A = os.getenv("REPO_A")
REPO_B = os.getenv("REPO_B")
REPO_C = os.getenv("REPO_C")
REPO_OWNER = os.getenv("REPO_OWNER")
B_WORKFLOW_FILE = os.getenv("B_WORKFLOW_FILE")
C_WORKFLOW_FILE = os.getenv("C_WORKFLOW_FILE")

github = github_client("github_conn")


def on_cross_repo(_):
    """Cross-repo trigger (completion of workflow in repo A triggers workflow in repo B)."""
    subscribe_to_event([REPO_A])
    trigger_workflow(REPO_B, B_WORKFLOW_FILE)


def on_fan_out(_):
    """Fan-out trigger (completion of workflow A triggers workflows B and C)."""
    subscribe_to_event([REPO_A])
    trigger_workflow(REPO_B, B_WORKFLOW_FILE)
    trigger_workflow(REPO_C, C_WORKFLOW_FILE)


def on_or_trigger(_):
    """OR trigger (completion of workflow A or B triggers workflow C)."""
    subscribe_to_event([REPO_A, REPO_B])
    trigger_workflow(REPO_C, C_WORKFLOW_FILE)


def on_fan_in(_):
    """Fan-in trigger (completion of workflows A and B triggers workflow C)."""
    completed_workflows = set()
    while len(completed_workflows) < 2:
        event = subscribe_to_event([REPO_A, REPO_B])
        completed_workflows.add(event.repository.name)
    trigger_workflow(REPO_C, C_WORKFLOW_FILE)


def trigger_workflow(repo_name, workflow_file, branch_or_tag="main"):
    """Trigger the workflow in the specified repository.

    Args:
        repo_name: The name of the repository.
        workflow_file: The name of the workflow file.
        branch_or_tag: The branch or tag name to trigger the workflow on.
    """
    repo = github.get_repo(f"{REPO_OWNER}/{repo_name}")
    workflow = repo.get_workflow(workflow_file)
    resp = workflow.create_dispatch(branch_or_tag)
    msg = "triggered successfully!" if resp else "failed to trigger."
    print(f"Workflow in {repo_name} {msg}")


def create_event_filter(repo_names, event_type="workflow_run", action="completed"):
    """Create a GitHub event filter string.

    Args:
        repo_names: A list of repository names to include in the filter.
        event_type: The type of event to filter.
        action: The action that the event should have.

    Returns:
        A formatted event filter string.
    """
    repo_filter = " || ".join(
        [f"data.workflow_run.repository.name == '{repo}'" for repo in repo_names]
    )
    return (
        f"event_type == '{event_type}' && ({repo_filter}) && data.action == '{action}'"
    )


def subscribe_to_event(repo_names):
    """Subscribe to a GitHub event and wait for the next event.

    Args:
        repo_names: A list of repository names to include in the event filter.

    Returns:
        The event that was received.
    """
    event_filter = create_event_filter(repo_names)
    sub = autokitteh.subscribe("github_conn", event_filter)
    return autokitteh.next_event(sub)

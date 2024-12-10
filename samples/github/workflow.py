"""Trigger GitHub Action workflows, and receive workflow events."""

from autokitteh.github import github_client


def start_github_action(event):
    """Start a GitHub action workflow.

    This function is preconfigured as the entry point for an AutoKitteh trigger.
    It will function correctly once a named workflow YAML file is created in a
    relevant GitHub repository under the ".github/workflows" directory.

    Example workflow YAML file:

        on: workflow_dispatch
        jobs:
          job-name:
            runs-on: ubuntu-latest
            steps:
              - run: echo "Do stuff"

    To fully utilize this trigger, ensure the workflow file is named appropriately
    (e.g., "dispatch.yml") and is configured for the intended events.

    Args:
        event: GitHub event data (e.g., a new pull request or push event).
    """
    repo = event.data.repository.full_name
    # TODO: ENG-1631
    ref = event.data.repository.default_branch  # Branch name or tag
    workflow_file = "dispatch.yml"  # .github/workflows/dispatch.yml

    g = github_client("github_conn")
    workflow = g.get_repo(repo).get_workflow(workflow_file)

    print("Triggering workflow:", workflow_file)
    # https://docs.github.com/en/rest/actions/workflows#create-a-workflow-dispatch-event
    workflow.create_dispatch(ref=ref)


def on_github_workflow_dispatch(event):
    """https://docs.github.com/en/webhooks/webhook-events-and-payloads#workflow_dispatch

    Args:
        data: GitHub event data.
    """
    print("Workflow dispatch:", event.data.workflow)
    print(event.data.inputs)


def on_github_workflow_job(event):
    """https://docs.github.com/en/webhooks/webhook-events-and-payloads#workflow_job

    Args:
        data: GitHub event data.
    """
    print(f"Workflow job {event.data.action}: {event.data.workflow_job.name}")
    print(event.data.workflow_job.html_url)


def on_github_workflow_run(event):
    """https://docs.github.com/en/webhooks/webhook-events-and-payloads#workflow_run

    Args:
        data: GitHub event data.
    """
    print(f"Workflow run {event.data.action}: {event.data.workflow_run.name}")
    print(event.data.workflow_run.html_url)

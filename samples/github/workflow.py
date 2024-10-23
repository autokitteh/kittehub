"""Trigger GitHub Action workflows, and receive workflow events."""

from autokitteh.github import github_client


def start_github_action(event):
    """Start a GitHub action workflow.

    See the following link for more information:
    https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#workflow_dispatch

    This function is preconfigured as the entry-point for an AutoKitteh trigger,
    but it's currently commented out in the "autokitteh.yaml" file. To activate it,
    uncomment the following lines:

        # - name: github_push
        #   connection: github_conn
        #   event_type: push
        #   call: workflow.py:start_github_action

    Additionally, it requires a named workflow YAML file to be present in a relevant GitHub repository.

    Example workflow YAML file (in the repo's ".github/workflows" directory):

        on: workflow_dispatch
        jobs:
          job-name:
            runs-on: ubuntu-latest
            steps:
              - run: echo "Do stuff"

    Args:
        event: GitHub event data (e.g. new pull request or push event).
    """
    repo = event.data.repo.full_name
    # TODO: ENG-1631
    ref = event.data.repo.default_branch  # Branch name or tag
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

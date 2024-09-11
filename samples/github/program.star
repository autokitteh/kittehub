"""This program demonstrates AutoKitteh's GitHub integration.

This program implements multiple entry-point functions that are triggered by
various GitHub webhook events, which are defined in the "autokitteh.yaml"
manifest file. It also executes various GitHub API calls.

API details:
- REST API referene: https://docs.github.com/en/rest
- Go client API: https://pkg.go.dev/github.com/google/go-github/v57/github

It also demonstrates using a custom builtin function (rand.intn) to generate
random integer numbers (based on https://pkg.go.dev/math/rand#Rand.Intn).

This program isn't meant to cover all available functions and events.
It merely showcases a few illustrative, annotated, reusable examples.

Starlark is a dialect of Python (see https://bazel.build/rules/language).
"""

load("@github", "github_conn")

# https://docs.github.com/en/rest/reactions/reactions#about-reactions
REACTIONS = ["+1", "-1", "laugh", "confused", "heart", "hooray", "rocket", "eyes"]

def on_github_issue_comment(data):
    """https://docs.github.com/en/rest/overview/github-event-types#issuecommentevent

    Based on the filter in the "autokitteh.yaml" manifest file,
    handle only *new* issue comments in this sample code
    (FYI, the other options are "edited" and "deleted").

    Args:
        data: GitHub event data.
    """

    # Add to each new issue comment a random reaction emoji.
    # rand.intn: https://pkg.go.dev/math/rand#Rand.Intn.
    reaction = REACTIONS[rand.intn(len(REACTIONS))]
    github_conn.create_reaction_for_issue_comment(
        owner = data.repo.owner.login,
        repo = data.repo.name,
        id = data.comment.id,
        content = reaction,
    )

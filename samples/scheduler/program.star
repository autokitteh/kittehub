"""This program demonstrates AutoKitteh's scheduler capabilities.

This program implements a single entry-point function, which is configured
in the "autokitteh.yaml" file as the receiver of "scheduler" events.

It also demonstrates using constant values which are set for each
AutoKitteh environment in the "autokitteh.yaml" manifest file.

Starlark is a dialect of Python (see https://bazel.build/rules/language).
"""

load("@slack", "slack_conn")
load("@github", "github_conn")

# Set in ""autokitteh.yaml"
load("env", "SLACK_CHANNEL_NAME_OR_ID", "GITHUB_OWNER", "GITHUB_REPO")

def on_cron_trigger():
    """An autokitteh cron schedule was triggered."""
    
    # fetch all PRs
    prs = github_conn.list_pull_requests(owner=GITHUB_OWNER, repo=GITHUB_REPO, state="open")

    # filter: skip DRAFT or WIP PRs
    active_prs = []
    for pr in prs:
        if pr.draft or any([k in pr.title.lower() for k in ("draft", "wip")]):
            continue
        active_prs.append(pr)

    now = time.now()
    good_updated_at = time.from_timestamp(now.unix - 1 * 60 * 60 * 24) # a day
    good_opened_at = time.from_timestamp(now.unix - 1 * 60 * 60 * 24 * 4) # 4 days

    msg = "Daily reminder about opened STALLED PRs:"
    for pr in active_prs:
        s = ""
        # check whether this PR is stalled - either opened or updated a long ago
        print(pr)
        if pr.created_at > good_opened_at or pr.updated_at > good_updated_at:
            s += "opened <%dh> ago, " % (now - pr.created_at).hours
            s += "last updated <%dh> ago" % (now - pr.updated_at).hours

        if len(s):
            msg += "\nPR: `%s`\n" % pr.title
            msg += "  %s\n" % pr.url
            msg += "  %s\n" % s
            slack_conn.chat_post_message(SLACK_CHANNEL_NAME_OR_ID, msg)

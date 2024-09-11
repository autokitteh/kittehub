"""This program demonstrates AutoKitteh's 2-way Atlassian Jira integration.

Atlassian Jira API documentation:
- https://docs.autokitteh.com/integrations/atlassian/jira/python
- https://docs.autokitteh.com/integrations/atlassian/jira/events
"""

from autokitteh.atlassian import jira_client


def on_jira_issue_created(event):
    issue_key = event.data.issue.key
    user_name = event.data.user.displayName

    jira = jira_client("jira_conn")
    jira.issue_add_comment(issue_key, "This issue was created by " + user_name)


def on_jira_comment_created(event):
    issue_key = event.data.issue.key
    comment = event.data.comment

    jira = jira_client("jira_conn")
    suffix = "\n\nThis comment was added by " + comment.author.displayName
    jira.issue_edit_comment(issue_key, comment.id, comment.body + suffix)

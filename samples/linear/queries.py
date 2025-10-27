"""GraphQL queries for interacting with Linear issues.

This module contains query strings for creating and managing issues via the Linear API.
"""

CREATE_ISSUE_QUERY = """
mutation CreateIssue($teamId: String!, $title: String!, $description: String) {
    issueCreate(
        input: {
            teamId: $teamId
            title: $title
            description: $description
        }
    ) {
        success
        issue {
            id
            url
        }
    }
}
"""


GET_ISSUE_QUERY = """
query GetIssue($id: String!) {
    issue(id: $id) {
        id
        title
        description
        state {
            name
        }
        priority
        createdAt
        updatedAt
        url
        assignee {
            name
        }
    }
}
"""

UPDATE_ISSUE_QUERY = """
mutation UpdateIssue($id: String!, $input: IssueUpdateInput!) {
    issueUpdate(
        id: $id
        input: $input
    ) {
        success
        issue {
            id
            title
        }
    }
}
"""

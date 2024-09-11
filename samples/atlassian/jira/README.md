# Atlassian Jira Sample

This [AutoKitteh](https://github.com/autokitteh/autokitteh) project
demonstrates 2-way integration with
[Jira](https://www.atlassian.com/software/jira/guides/).

Jira API documentation:

- [REST API](https://developer.atlassian.com/cloud/jira/platform/rest/v3/intro/)
- ["Atlassian Python API" Python library](https://atlassian-python-api.readthedocs.io/)
- ["Jira" Python library](https://jira.readthedocs.io/)

Python code samples:

- [Atlassian Python API](https://github.com/atlassian-api/atlassian-python-api/tree/master/examples/jira)
- [Jira](https://github.com/pycontribs/jira/tree/main/examples)

This program isn't meant to cover all available functions and events. It
merely showcases a few illustrative, annotated, reusable examples.

## Instructions

1. Deploy the manifest file:

   ```shell
   ak deploy --manifest samples/jira/autokitteh.yaml
   ```

2. Follow the instructions in the `ak` CLI tool's output:

   ```
   Connection created, but requires initialization.
   Please run this to complete:

   ak connection init <connection ID>
   ```

3. Create a new issue in Jira, and check its comments

## Connection Notes

AutoKitteh supports three connection modes:

- User impersonation with:

  - [API token](https://id.atlassian.com/manage-profile/security/api-tokens)
    (available only in Atlassian Cloud)

  - [Personal Access Token (PAT)](https://confluence.atlassian.com/enterprise/using-personal-access-tokens-1026032365.html)
    (available only in on-prem servers)

- [OAuth 2.0 (3LO) app](https://developer.atlassian.com/cloud/jira/platform/oauth-2-3lo-apps/)

  - [AutoKitteh guide: configuring Atlassian integrations](https://docs.autokitteh.com/integrations/atlassian/config)

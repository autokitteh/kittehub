# GitHub Sample

This [AutoKitteh](https://github.com/autokitteh/autokitteh) project
demonstrates 2-way integration with [GitHub](https://github.com).

The file [`program.star`](./program.star) implements multiple entry-point
functions that are triggered by various GitHub webhook events, which are
defined in the [`autokitteh.yaml`](./autokitteh.yaml) manifest file. It also
executes various GitHub API calls.

The file [`workflow.star`](./workflow.star) demonstrates triggering GitHub
Action workflows, and receiving workflow events.

GitHub API details:

- [REST API reference](https://docs.github.com/en/rest)
- [Go client API](https://pkg.go.dev/github.com/google/go-github/v57/github)

It also demonstrates using a custom builtin function (`rand.intn`) to generate
random integer numbers, based on <https://pkg.go.dev/math/rand#Rand.Intn>.

This project isn't meant to cover all available functions and events. It
merely showcases a few illustrative, annotated, reusable examples.

## Instructions

1. [Configure your GitHub integration](https://docs.autokitteh.com/integrations/github).

2. Via the `ak` CLI tool, or the AutoKitteh VS Code extension, deploy the
   `autokitteh.yaml` manifest file

## Connection Notes

AutoKitteh supports 2 connection modes:

- Personal Access Token (PAT - either fine-grained or classic) + manually-configured
  webhook

  - [Authenticating with a personal access token](https://docs.github.com/en/rest/authentication/authenticating-to-the-rest-api#authenticating-with-a-personal-access-token)
  - [Managing your personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)
  - [Setting a PAT policy for your organization](https://docs.github.com/en/organizations/managing-programmatic-access-to-your-organization/setting-a-personal-access-token-policy-for-your-organization)
  - [Endpoints available for fine-grained PATs](https://docs.github.com/en/rest/authentication/endpoints-available-for-fine-grained-personal-access-tokens)

- GitHub App (installed and authorized in step 1 above)

  - [About using GitHub Apps](https://docs.github.com/en/apps/using-github-apps/about-using-github-apps)

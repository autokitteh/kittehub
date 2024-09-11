# Scheduler (Cron) Sample

This project demonstrates
[AutoKitteh](https://github.com/autokitteh/autokitteh)'s
cron-like scheduler.

It scans a specific GitHub repo on a daily basis to identify stalled PRs. If
any are found, it sends a message about them to a specific Slack channel.

## API Documentation

- [Cron expression format](https://pkg.go.dev/github.com/robfig/cron/v3#hdr-CRON_Expression_Format)
  ("\* \* \* \* \*")

- [Cron extended expression format](https://pkg.go.dev/github.com/robfig/cron/v3#hdr-Alternative_Formats)
  (includes seconds and minutes)

- [Predefined schedules and intervals](https://pkg.go.dev/github.com/robfig/cron#hdr-Predefined_schedules)
  ("@" format)

  - `@yearly`/`@annually`, `@monthly`, `@weekly`, `@daily`/`@midnight`, `@hourly`
  - `@every 1h30m10s`

- [Crontab.guru - cron schedule expression editor](https://crontab.guru/)

## Setup Instructions

1. Install and start a
   [self-hosted AutoKitteh server](https://docs.autokitteh.com/get_started/quickstart),
   or use AutoKitteh Cloud

2. Optional for self-hosted servers (preconfigured in AutoKitteh Cloud):

   - [Enable GitHub connections to use a GitHub app](https://docs.autokitteh.com/integrations/github/config)
   - [Enable Slack connections to use an OAuth v2 app](https://docs.autokitteh.com/integrations/slack/config)

3. Run this command to clone the Kittehub repository, which contains this
   project:

   ```shell
   git clone https://github.com/autokitteh/kittehub.git
   ```

4. Set these variables in this project's [autokitteh.yaml](./autokitteh.yaml)
   manifest file:

   - `GITHUB_OWNER` and `GITHUB_REPO`
   - `SLACK_CHANNEL_NAME_OR_ID`

5. Run this command to deploy this project's manifest file:

   ```shell
   ak deploy --manifest kittehub/samples/scheduler/autokitteh.yaml
   ```

6. Initialize this project's connections:

   - GitHub: with a GitHub app using OAuth 2.0 (based on step 2), or PATs
     (fine-grained or classic) and/or manually-configured webhooks
   - Slack: with an OAuth v2 app (based on step 2), or a Socket Mode app

> [!TIP]
> The exact CLI commands to do so (`ak connection init ...`) will appear in
> the output of the `ak deploy` command from step 5 when you create the
> project on the server, i.e. when you run that command for the first time.

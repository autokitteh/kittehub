"""Main workflow for the Kubernetes sheet dashboard."""

from os import getenv
import re

from autokitteh import Event, start

from do import do
import kube
import sheet
import slack


_slack_cmd_prefix = f"!{getenv('INVOCATION_CMD', 'dd')} "

_slack_cmd_re = re.compile(r"^([\w_-]+) (\w+) ?(.*)$")


def on_poll_sheet(_):
    ds = sheet.get_deployments()
    print(ds)

    for d in ds:
        state = kube.get_deployment_state(d.name)

        print(f"{d.name}: {state}")

        sheet.update_deployment_current_state(d.row_num, state)

        if d.op:
            sheet.update_deployment_status(d.row_num, "", f"pending: {d.op}")
            sid = start("do.py:do_event", {"deployment": d.__dict__})
            print(f"{d.name}: do_event {d.op} -> {sid}")


def on_slack_message(event: Event) -> None:
    ds = sheet.get_deployments()
    print(ds)

    text = event.data.text

    if not text.startswith(_slack_cmd_prefix):
        print("irrelevant")
        return

    cmd = text.removeprefix(_slack_cmd_prefix)
    print(f"slack({event.data.channel},{event.data.thread_ts}): {cmd}")

    slack_dst = {
        "channel": event.data.channel,
        "thread_ts": event.data.ts,
    }

    match = _slack_cmd_re.match(cmd)
    if not match:
        slack.send(text=f"Invalid command: {cmd}", **slack_dst)
        return

    name, op, arg = match.groups()

    d = next((d for d in ds if d.name == name), None)

    if not d:
        slack.send(text=f"Unknown deployment: {name}", **slack_dst)
        return

    do(d, op, arg, slack_dst, event.session_id)

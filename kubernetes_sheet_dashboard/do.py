from autokitteh import Event, subscribe, next_event

import data
import kube
import sheet
import slack


def do_event(event: Event) -> None:
    d = data.Deployment(**event.data["deployment"])

    do(
        d=d,
        op=d.op,
        slack_dst={},
        arg="",
        id=event.session_id,
    )


def do(d, op, arg, slack_dst, id) -> None:
    """Perform the operation on the deployment."""
    print(f"{slack_dst} - {d.name} #{d.row_num}: do {d.op}({arg})")

    def notify(msg: str) -> None:
        if slack_dst:
            slack.send(text=msg, **slack_dst)

        for ch in d.slack:
            slack.send(text=msg, channel=ch)

    def update(status):
        msg = f"🔨 Deployment {d.name}: {op} -> {status}"
        print(msg)
        notify(msg)
        sheet.update_deployment_status(d.row_num, "", status)

    def approve(what: str) -> bool:
        update(f"approving {what}...")

        ddcmd = f"%dd_{id.split('_')[1]}"

        sub = subscribe(
            "slack",
            f"data.type == 'message' && data.text.startsWith('{ddcmd}')",
        )

        notify(
            f"""Requires approval: {what}
Approve: `{ddcmd} approve`
Deny: `{ddcmd} deny`
""",
        )

        evt = next_event(sub)
        match evt.text.split(" ", 1)[-1]:
            case "approve":
                update(f"{what} approved by <@{evt.user}>")
                return True
            case "deny":
                update(f"denied: {what}")
                return False
            case _:
                update(f"???: {evt.text}, denying")
                return False

    match op:
        case "nop":
            update("nopped")
        case "restart":
            if not approve("restart"):
                return
            _restart(d.name, update)
        case "scale":
            n = int(arg) if arg != "" else d.desired_replicas
            if not approve(f"scale {n}"):
                return
            _scale(d.name, n, update)
        case "image":
            image = arg if arg != "" else d.desired_image
            if not approve(f"image {image}"):
                return
            _image(d.name, image, update)
        case _:
            update(f"???: {d.op}")


def _restart(name: str, update) -> None:
    update("restarting...")

    try:
        kube.restart_deployment(name)
    except kube.ApiException as e:
        update(f"error: {e}")
        return

    update("restarted")


def _scale(name: str, replicas: int | None, update) -> None:
    if replicas is None:
        update("error: invalid scale")
        return

    update(f"scale->{replicas}...")

    try:
        kube.scale(name, replicas)
    except kube.ApiException as e:
        update(f"error: {e}")
        return

    update(f"scale={replicas}")


def _image(name: str, image: str, update) -> None:
    if not image:
        update("error: invalid image")
        return

    update(f"image->{image}...")

    try:
        kube.image(name, image)
    except kube.ApiException as e:
        update(f"error: {e}")
        return

    update(f"image={image}")

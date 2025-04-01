"""Kubernetes"""

import datetime

from autokitteh import activity
import kubernetes

from data import CurrentState


kubernetes.config.load_kube_config()  # TODO: from vars.
apps = kubernetes.client.AppsV1Api()

_NAMESPACE = "default"


ApiException = kubernetes.client.exceptions.ApiException


class Error(Exception):
    """Base class for all errors."""

    def __init__(self, message: str) -> None:
        super().__init__(message)


# `apps.read_namespaced_deployment`` returns a big object, but we need
# only few of the fields back. Having everything in an activity
# avoids serializing the whole object, but just the fields we're
# interested in.
@activity
def get_deployment_state(name: str) -> CurrentState | None:
    """Get the state of a deployment."""
    try:
        d = apps.read_namespaced_deployment(name, _NAMESPACE)
    except ApiException as e:
        if e.status == 404:
            return None
        raise e

    return CurrentState(
        image=d.spec.template.spec.containers[0].image,
        desired_replicas=d.status.replicas,
        available_replicas=d.status.available_replicas,
        unavailable_replicas=d.status.unavailable_replicas,
        updated_replicas=d.status.updated_replicas,
        ready_replicas=d.status.ready_replicas,
    )


def restart_deployment(name: str) -> None:
    """Restart a deployment."""
    now = str(datetime.datetime.now(datetime.UTC).isoformat("T") + "Z")

    body = {
        "spec": {
            "template": {
                "metadata": {"annotations": {"kubectl.kubernetes.io/restartedAt": now}}
            }
        }
    }

    apps.patch_namespaced_deployment(name, _NAMESPACE, body)


def scale(name: str, replicas: int) -> None:
    """Scale a deployment."""
    apps.patch_namespaced_deployment_scale(
        name, _NAMESPACE, {"spec": {"replicas": replicas}}
    )


def image(name: str, image: str) -> None:
    """Change the image of a deployment."""
    body = {
        "spec": {
            "template": {"spec": {"containers": [{"name": "image", "image": image}]}}
        }
    }

    apps.patch_namespaced_deployment(name, _NAMESPACE, body)

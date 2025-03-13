"""Create Zoom meetings."""

from autokitteh.zoom import zoom_client


zoom = zoom_client("zoom_conn")


def create_meeting(topic):
    resp = zoom.post(
        "https://api.zoom.us/v2/users/me/meetings",
        json={"topic": topic},
    )
    resp.raise_for_status()
    return resp.json().get("join_url")

"""MS Azure DevOps Pipelines -> MS Teams via Azure Bot"""

from os import getenv
from autokitteh import subscribe, next_event
from autokitteh.azurebot import azurebot_client

from azure.devops.connection import Connection
from azure.devops.v7_1.build.models import Build
from msrest.authentication import BasicAuthentication


_CHANNEL_CONVO_ID = getenv("CHANNEL_CONVO_ID")


devops_clients = Connection(
    base_url=f"https://dev.azure.com/{getenv('AZURE_DEVOPS_ORG')}",
    creds=BasicAuthentication("", getenv("AZURE_DEVOPS_PAT")),
).clients

build_client = devops_clients.get_build_client()

bot_client = azurebot_client("bot")


def on_azuredev_webhook(event):
    data = event.data.body.json

    activity_id = bot_client.send_conversation_activity(
        {
            "type": "message",
            "text": data["detailedMessage"]["markdown"],
        },
        conversation_id=_CHANNEL_CONVO_ID,
    )["id"]

    convo_id = f"{_CHANNEL_CONVO_ID};messageid={activity_id}"

    build_id, project_name = (
        data["resource"]["id"],
        data["resource"]["project"]["name"],
    )

    print(f"Build completed: {build_id} in {project_name}")

    sub = subscribe("bot", filter=f"data.conversation.id='{convo_id}'")

    while True:
        evt = next_event(sub)
        print(evt)

        text = evt.text.lower()

        if "retry" in text:
            build = build_client.get_build(project=project_name, build_id=build_id)

            new_build = build_client.queue_build(
                build=Build(
                    definition=build.definition,
                    source_branch=build.source_branch,
                    source_version=build.source_version,
                    parameters=build.parameters,
                ),
                project=project_name,
            )

            bot_client.send_conversation_activity(
                {"type": "message", "text": f"New build: {new_build.url}"},
                conversation_id=convo_id,
            )

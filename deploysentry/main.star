load("env", "DEPLOYSENTRY_ADDR", "INITIAL_RATIO", "RATIO_INCREMENT", "STEP_DURATION")
load("@grpc", "grpc")
load("@http", "http")
load("@slack", "slack")

MAX_ERROR_RATE = 5

def on_slack_app_mention(data):
    channel = data.channel

    parts = data.text.split(" ")

    if parts[1] != "deploy":
        return

    svc, version = parts[2], parts[3]

    print(svc, version)

    _deploy(channel, svc, version)

    for r in range(0, 100, int(RATIO_INCREMENT)):
        result = http.get("http://{}/check".format(DEPLOYSENTRY_ADDR), params={"svc": svc}).body_json
        rate = result['error_rate']
        slack.chat_post_message(channel, "error rate: {}".format(rate))

        if rate > MAX_ERROR_RATE:
            slack.chat_post_message(channel, "error rate too high, aborting deployment")
            _set_ratio(channel, svc, version, 0)
            return

        _set_ratio(channel, svc, version, r)
        sleep(STEP_DURATION)

    _set_ratio(channel, svc, version, 100)
    slack.chat_post_message(channel, "deployment complete, yay!")


def _deploy(channel, svc, version):
    slack.chat_post_message(channel, "deploying {}#{}".format(svc, version))

    grpc.call(
        host=DEPLOYSENTRY_ADDR,
        service="autokitteh.deploysentry.api.v1.DeploySentryService",
        method="Deploy",
        payload={
            "svc": svc,
            "version": version,
        },
    )

def _set_ratio(channel, svc, version, ratio):
    slack.chat_post_message(channel, "setting ratio of {}#{} to {}%".format(svc, version, ratio))

    grpc.call(
        host=DEPLOYSENTRY_ADDR,
        service="autokitteh.deploysentry.api.v1.DeploySentryService",
        method="SetRatio",
        payload={
            "svc": svc,
            "version": version,
            "ratio": ratio,
        },
    )

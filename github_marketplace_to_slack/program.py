"""Forward GitHub Marketplace webhook notifications to a Slack channel.

GitHub API documentation:
- https://docs.github.com/en/apps/github-marketplace/listing-an-app-on-github-marketplace/configuring-a-webhook-to-notify-you-of-plan-changes

HTTP API documentation:
- https://docs.autokitteh.com/integrations/http/events

Slack API documentation:
- https://docs.autokitteh.com/integrations/slack/python
"""


def on_webhook_notification(event):
    # TODO:
    # https://docs.github.com/en/webhooks/webhook-events-and-payloads#marketplace_purchase
    # https://docs.github.com/en/webhooks/webhook-events-and-payloads#ping
    # https://docs.github.com/en/webhooks/webhook-events-and-payloads#delivery-headers
    # https://docs.github.com/en/webhooks/using-webhooks/validating-webhook-deliveries

    # Headers example:
    # Content-Type      application/x-www-form-urlencoded
    # X-Github-Event    ping
    # X-Github-Hook-Id  500801516
    # X-Github-Hook-Installation-Target-Id    18932
    # X-Github-Hook-Installation-Target-Type  marketplace::listing
    # X-Hub-Signature      sha1=.....
    # X-Hub-Signature-256  sha256=.....
    for key in sorted(event.data.headers):
        print(f"{key}: {event.data.headers[key]}")

    # JSON payload example:
    # {
    #     "zen": "Encourage flow.",
    #     "hook_id": 500801516,
    #     "hook": {
    #         "type": "Marketplace::Listing",
    #         "id": 500801516,
    #         "name": "web",
    #         "active": true,
    #         "events": [
    #             "*"
    #         ],
    #         "config": {
    #             "content_type": "form",
    #             "secret": "********",
    #             "url": "https://autokitteh.ngrok.dev/webhooks/2HvQPkQndqa4anbNEp3xfP",
    #             "insecure_ssl": "0"
    #         },
    #         "updated_at": "2024-09-09T19:10:16Z",
    #         "created_at": "2024-09-09T19:10:16Z",
    #         "marketplace_listing_id": 18932
    #     },
    #     "sender": {
    #         "login": "daabr",
    #         "id": 32577337,
    #         "node_id": "MDQ6VXNlcjMyNTc3MzM3",
    #         "avatar_url": "https://avatars.githubusercontent.com/u/32577337?v=4",
    #         "gravatar_id": "",
    #         "url": "https://api.github.com/users/daabr",
    #         "html_url": "https://github.com/daabr",
    #         "followers_url": "https://api.github.com/users/daabr/followers",
    #         "following_url": "https://api.github.com/users/daabr/following{/other_user}",
    #         "gists_url": "https://api.github.com/users/daabr/gists{/gist_id}",
    #         "starred_url": "https://api.github.com/users/daabr/starred{/owner}{/repo}",
    #         "subscriptions_url": "https://api.github.com/users/daabr/subscriptions",
    #         "organizations_url": "https://api.github.com/users/daabr/orgs",
    #         "repos_url": "https://api.github.com/users/daabr/repos",
    #         "events_url": "https://api.github.com/users/daabr/events{/privacy}",
    #         "received_events_url": "https://api.github.com/users/daabr/received_events",
    #         "type": "User",
    #         "site_admin": false
    #     }
    # }
    print(event.data.body)

import json

import requests

WEBHOOK_URL = "https://hooks.slack.com/services/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"


def post_to_slack(text: str):
    requests.post(WEBHOOK_URL, data=json.dumps({
        "text": text,
        "icon_emoji": ":robot_face:",
        "username": "tomo-vaccination-bot"
    }))

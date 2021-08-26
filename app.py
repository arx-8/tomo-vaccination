import json
import os

import requests
from bs4 import BeautifulSoup
from chalice import Chalice
from chalice.app import CloudWatchEvent, Rate

# constants
LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
LINE_ROOM_ID = os.environ["LINE_ROOM_ID"]
SLACK_INCOMING_WEBHOOK_URL = os.environ["SLACK_INCOMING_WEBHOOK_URL"]
TARGET_URL = os.environ["TARGET_URL"]

# init chalice
app = Chalice(app_name="tomo-vaccination")


def log(text: str) -> None:
    """
    log for CloudWatch
    """
    # TODO replace Chalice.log.error()
    print("***" + text)


def post_to_slack(text: str) -> None:
    res = requests.post(SLACK_INCOMING_WEBHOOK_URL, data=json.dumps({
        "text": text,
        "icon_emoji": ":robot_face:",
        "username": "tomo-vaccination-bot"
    }))

    if not res.status_code == 200:
        log("post_to_slack unexpected error: " + res.text)


def post_to_line(text: str) -> None:
    res = requests.post(
        "https://api.line.me/v2/bot/message/push",
        data=json.dumps({
            "to": LINE_ROOM_ID,
            "messages": [
                {
                    "type": "text",
                    "text": text
                }
            ]
        }),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}",
        }
    )

    if not res.status_code == 200:
        log("post_to_line unexpected error: " + res.text)
        post_to_slack("post_to_line unexpected error: " + res.text)


def fetch_is_available_to_apply() -> bool:
    res = requests.get(TARGET_URL)
    if not res.status_code == 200:
        log("Cannot to connect site: " + res.text)
        post_to_slack("Cannot to connect site: " + res.text)
        return False

    try:
        soup = BeautifulSoup(res.text, "html.parser")
        maybe_tag = soup.select_one("#frm > .c-box--save.note_box")
        if maybe_tag is None:
            # 申込開始した時、そもそもこの要素がないのでは？の処理
            return True

        text = maybe_tag.get_text().strip()
        return not (text in "申込期間ではありません。")
    except Exception as e:
        log("Unexpected scraping error: " + str(e))
        post_to_slack("<!channel> Unexpected scraping error: " + str(e))
        return False


@app.schedule(Rate(5, unit=Rate.MINUTES))
def check(event: CloudWatchEvent):
    is_available = fetch_is_available_to_apply()

    if is_available:
        # 開始前はどうでもいいので、開始した時だけ通知する
        post_to_line(f"予約開始かもよ: {TARGET_URL}")
    else:
        post_to_line(f"まだだよ: {TARGET_URL}")

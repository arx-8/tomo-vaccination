import json
import logging
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
app.log.setLevel(logging.INFO)


def post_to_slack(text: str) -> None:
    res = requests.post(SLACK_INCOMING_WEBHOOK_URL, data=json.dumps({
        "text": text,
        "icon_emoji": ":robot_face:",
        "username": "tomo-vaccination-bot"
    }))

    if not res.status_code == 200:
        app.log.error(f"post_to_slack unexpected error: {res.text}")


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
        app.log.error(f"post_to_line unexpected error: {res.text}")
        post_to_slack(f"post_to_line unexpected error: {res.text}")


def fetch_is_available_to_apply() -> bool:
    res = requests.get(TARGET_URL, {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 Edg/81.0.416.72",
    })
    if not res.status_code == 200:
        app.log.error(f"Cannot to connect site: {res.text}")
        post_to_slack(f"Cannot to connect site: {res.text}")
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
        app.log.error(f"Unexpected scraping error: {str(e)}")
        post_to_slack(f"<!channel> Unexpected scraping error: {str(e)}")
        return False


@app.schedule(Rate(5, unit=Rate.MINUTES))
def check(event: CloudWatchEvent):
    is_available = fetch_is_available_to_apply()

    if is_available:
        # 開始前はどうでもいいので、開始した時だけ通知する
        post_to_line(f"予約開始かもよ: {TARGET_URL}")
    else:
        app.log.info("It seems not yet")

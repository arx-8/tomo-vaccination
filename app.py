import json

import requests
from bs4 import BeautifulSoup
from chalice import Chalice
from chalice.app import CloudWatchEvent, Rate

app = Chalice(app_name="tomo-vaccination")


WEBHOOK_URL = "https://hooks.slack.com/services/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"


def post_to_slack(text: str):
    requests.post(WEBHOOK_URL, data=json.dumps({
        "text": text,
        "icon_emoji": ":robot_face:",
        "username": "tomo-vaccination-bot"
    }))


def fetch_is_available_to_apply() -> bool:
    target_url = "https://s-kantan.jp/city-gyoda-saitama-u/offer/offerDetail_initDisplay.action?tempSeq=25956&accessFrom="
    res = requests.get(target_url)
    soup = BeautifulSoup(res.text, "html.parser")

    # TODO targe が存在しなかった場合のエラー処理
    # TODO targe 文言が変わった場合のエラー処理
    # TODO 申込開始した時、そもそもこの要素がないのでは？の処理
    text = soup.select_one("#frm > .c-box--save.note_box").get_text().strip()

    return not (text in "申込期間ではありません。")


@app.schedule(Rate(1, unit=Rate.MINUTES))
def check(event: CloudWatchEvent):
    # TODO FIXME
    is_available = fetch_is_available_to_apply()

    post_to_slack(str(is_available) + ":" + str(event.to_dict()))

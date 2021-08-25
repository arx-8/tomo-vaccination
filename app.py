import json

import requests
from bs4 import BeautifulSoup
from chalice import Chalice
from chalice.app import CloudWatchEvent, Rate

app = Chalice(app_name="tomo-vaccination")


def post_to_slack(text: str):
    requests.post("https://hooks.slack.com/services/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", data=json.dumps({
        "text": text,
        "icon_emoji": ":robot_face:",
        "username": "tomo-vaccination-bot"
    }))


def fetch_is_available_to_apply() -> bool:
    target_url = "https://s-kantan.jp/city-gyoda-saitama-u/offer/offerDetail_initDisplay.action?tempSeq=25956&accessFrom="
    res = requests.get(target_url)
    soup = BeautifulSoup(res.text, "html.parser")

    maybe_tag = soup.select_one("#frm > .c-box--save.note_box")
    if maybe_tag is None:
        # 申込開始した時、そもそもこの要素がないのでは？の処理
        return True

    text = maybe_tag.get_text().strip()

    return not (text in "申込期間ではありません。")


@app.schedule(Rate(5, unit=Rate.MINUTES))
def check(event: CloudWatchEvent):
    is_available = fetch_is_available_to_apply()

    if is_available:
        post_to_slack("<!channel> 予約開始かもよ")
    else:
        post_to_slack("no")

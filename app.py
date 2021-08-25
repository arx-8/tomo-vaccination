import json

import requests
from bs4 import BeautifulSoup
from chalice import Chalice
from chalice.app import CloudWatchEvent, Rate

app = Chalice(app_name="tomo-vaccination")


def log(text: str) -> None:
    """
    log for CloudWatch
    """
    print("***" + text)


def post_to_slack(text: str):
    res = requests.post("https://hooks.slack.com/services/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", data=json.dumps({
        "text": text,
        "icon_emoji": ":robot_face:",
        "username": "tomo-vaccination-bot"
    }))

    if not res.status_code == 200:
        log("WebHook unexpected error: " + res.text)


def fetch_is_available_to_apply() -> bool:
    target_url = "https://s-kantan.jp/city-gyoda-saitama-u/offer/offerDetail_initDisplay.action?tempSeq=25956&accessFrom="
    res = requests.get(target_url)
    if not res.status_code == 200:
        log("Cannot to connect site: " + res.text)
        post_to_slack("<!channel> Unexpected scraping error: " + str(e))
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
        post_to_slack("<!channel> 予約開始かもよ")
    else:
        log("It seems not yet")

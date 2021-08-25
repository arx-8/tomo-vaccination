import requests
from bs4 import BeautifulSoup

from slack import post_to_slack

target_url = "https://s-kantan.jp/city-gyoda-saitama-u/offer/offerDetail_initDisplay.action?tempSeq=25956&accessFrom="
res = requests.get(target_url)
soup = BeautifulSoup(res.text, "html.parser")

# TODO targe が存在しなかった場合のエラー処理
# TODO targe 文言が変わった場合のエラー処理
# TODO 申込開始した時、そもそもこの要素がないのでは？の処理
text = soup.select_one("#frm > .c-box--save.note_box").get_text().strip()

is_available_to_apply = not (text in "申込期間ではありません。")

if is_available_to_apply:
    post_to_slack("ok")
else:
    post_to_slack("no")

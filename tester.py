import codecs
import json

import requests


def post_to_line():
    res = requests.post(
        "https://api.line.me/v2/bot/message/push",
        data=json.dumps({
            "to": "U1",
            "messages": [
                {
                    "type": "text",
                    "text": "Hello, world1"
                }
            ]
        }),
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer TOKEN",
        }
    )

    print(res.status_code)
    print(res.text)


def check_ua():
    res = requests.get("http://taruo.net/e/?", headers={
        "User-Agent": "Mozilla/5.0"
    })

    decoded = res.text\
        .replace("\xbe", "")\
        .replace("\xbd", "")\
        .replace("\xd0", "")\
        .replace("\xb3", "")\
        .encode("euc_jp").decode("utf_8")

    print(decoded)


check_ua()


"""
curl -v -X POST https://api.line.me/v2/bot/message/push \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer TOKEN' \
-d '{
    "to": "G1",
    "messages":[
        {
            "type":"text",
            "text":"Hello, world1"
        }
    ]
}'


user_id: U1

group_id: G1

"""

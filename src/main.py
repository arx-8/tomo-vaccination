import requests
from bs4 import BeautifulSoup

target_url = "https://www.yahoo.co.jp/"
res = requests.get(target_url)
soup = BeautifulSoup(res.text, "html.parser")

title_text = soup.find('title').get_text()
print(title_text)

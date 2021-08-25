from chalice import Chalice
from chalice.app import CloudWatchEvent, Rate

from src.scraper import fetch_is_available_to_apply
from src.slack import post_to_slack

app = Chalice(app_name="tomo-vaccination")


@app.schedule(Rate(1, unit=Rate.MINUTES))
def check(event: CloudWatchEvent):
    # TODO FIXME
    is_available = fetch_is_available_to_apply()

    post_to_slack(str(is_available) + ":" + str(event.to_dict()))

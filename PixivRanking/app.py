import falcon
from .daily_illust_rankings_interface import DailyIllustRankingsInterface

app = application = falcon.App()
# note: Gunicorn, by default, expects this to be called "application"

image = DailyIllustRankingsInterface()
app.add_route("/image", image)
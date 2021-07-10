import falcon
from .daily_illust_rankings_interface import DailyIllustRankingsInterface

class CORSMiddleware:
    def process_request(self, req, resp):
        resp.set_header('Access-Control-Allow-Origin', 'https://www.pixivquiz.net')

app = application = falcon.App(middleware=[CORSMiddleware()])
# note: Gunicorn, by default, expects this to be called "application"

# app = application = falcon.App(middleware=falcon.CORSMiddleware(
#     allow_origins='https://www.pixivquiz.net', allow_credentials='*'))
# これだとうまくいかなかった。cf: https://falcon.readthedocs.io/en/3.0.1/api/cors.html


image = DailyIllustRankingsInterface()
app.add_route("/image", image)
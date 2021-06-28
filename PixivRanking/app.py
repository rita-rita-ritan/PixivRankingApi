import falcon
from .images import Resource

app = application = falcon.App()
# note: Gunicorn, by default, expects this to be called "application"

images = Resource()
app.add_route("/images", images)
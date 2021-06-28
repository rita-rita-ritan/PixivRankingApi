import json
import falcon
import random

class Resource:
    def on_get(self, req, resp):
        with open("PixivRanking/data/daily-illust-ranking.json") as f:
            images = json.load(f)

        random_index = random.randrange(len(images))
        image = images[random_index]

        resp.text = json.dumps(image, ensure_ascii=False)
        resp.status = falcon.HTTP_200  # can be omitted because 200 is the default

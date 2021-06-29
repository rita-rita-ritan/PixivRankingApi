import json
import falcon
import random
class DailyIllustRankingsInterface:
    def on_get(self, req, resp):
        with open("PixivRanking/data/daily_illust_rankings.json") as f:
            images = json.load(f)
        
        timestamp = images["timestamp"]

        random_image_id = random.randrange(1, len(images))  # imagesにtimestampが含まれることに注意
        image = images[str(random_image_id)]

        resp.text = json.dumps({"timestamp": timestamp, **image}, ensure_ascii=False)
        resp.status = falcon.HTTP_200  # can be omitted because 200 is the default
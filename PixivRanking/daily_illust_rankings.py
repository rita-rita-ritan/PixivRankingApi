import requests
from bs4 import BeautifulSoup
import json
import time
import datetime

class DailyIllustRankings:
    works = {}
    len_works = 50
    timestamp = ""

    def __init__(self):
        for id in range(1, self.len_works + 1):
            self.works[id] = {}

    def get_now_time(self):
        JST = datetime.timezone(datetime.timedelta(hours=9))  # 日本標準時 (Japan Standard Time)
        dt_now_jst = datetime.datetime.now(JST)
        self.timestamp = dt_now_jst.strftime('%Y/%m/%d %H:%M')
    
    def get_work_urls_from_ranking(self):
        source_html = requests.get('https://www.pixiv.net/ranking.php?mode=daily&content=illust')
        self.get_now_time()
        soup = BeautifulSoup(source_html.text, "html.parser")
        for i, work_html in enumerate(soup.select(".work")):
            self.works[i + 1]["work_url"] = "https://www.pixiv.net" + work_html["href"]

    def get_opengraph(self, id, work_url):
        # id (int): Ranking in Daily Illust Rankings. 1-indexed

        source_html = requests.get(work_url)
        soup = BeautifulSoup(source_html.text, "html.parser")

        # head > meta property="og:image"
        og_image_url = soup.select_one('meta[property="og:image"]')["content"]

        # head > meta property="og:title"
        og_title = [v.strip() for v 
            in soup.select_one('meta[property="og:title"]')["content"].split('-')]
        og_image_title = ''.join(og_title[0].split()[1:])
        og_creator_name = og_title[-2][:-5]

        self.works[id]["og_image_url"] = og_image_url
        self.works[id]["og_image_title"] = og_image_title
        self.works[id]["og_creator_name"] = og_creator_name

    def get_opengraphs(self):
        for id in self.works:
            time.sleep(10)
            self.get_opengraph(id, self.works[id]["work_url"])

    def save_as_json(self):
        with open("data/daily_illust_rankings.json", "w") as f:
            json.dump({"timestamp": self.timestamp, **self.works}, f, indent=4)

if __name__ == "__main__":
    # for test
    ranking = DailyIllustRankings()
    ranking.get_work_urls_from_ranking()
    ranking.get_opengraphs()
    ranking.save_as_json()
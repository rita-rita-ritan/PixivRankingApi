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
        for rank in range(1, self.len_works + 1):
            self.works[rank] = {"rank": rank}

    def get_now_time(self):
        JST = datetime.timezone(datetime.timedelta(hours=9))  # 日本標準時 (Japan Standard Time)
        dt_now_jst = datetime.datetime.now(JST)
        self.timestamp = dt_now_jst.strftime('%Y/%m/%d %H:%M')
    
    def get_work_urls_from_ranking(self):
        source_html = requests.get('https://www.pixiv.net/ranking.php?mode=daily&content=illust')
        self.get_now_time()
        soup = BeautifulSoup(source_html.text, "html.parser")

        creator_names = soup.select(".user-name")
        creator_urls = soup.select(".user-container")
        work_titles = soup.select(".title")
        work_urls = ["https://www.pixiv.net" + work_html["href"] 
                        for work_html in soup.select(".work")]

        for i in range(self.len_works):
            self.works[i + 1]["creator_name"] = creator_names[i].get_text()
            self.works[i + 1]["creator_url"] = "https://www.pixiv.net" + creator_urls[i]["href"]
            self.works[i + 1]["work_title"] = work_titles[i].get_text()
            self.works[i + 1]["work_url"] = work_urls[i]

    def get_work_opengraph(self, rank, work_url):
        # rank:int (1-indexed)

        source_html = requests.get(work_url)
        soup = BeautifulSoup(source_html.text, "html.parser")

        # head > meta property="og:image"
        og_image_url = soup.select_one('meta[property="og:image"]')["content"]
        self.works[rank]["opengraph_work_image_url"] = og_image_url

    def get_creator_opengraph(self, rank, work_url):
        # rank:int (1-indexed)

        source_html = requests.get(work_url)
        soup = BeautifulSoup(source_html.text, "html.parser")

        # head > meta property="og:image"
        og_image_url = soup.select_one('meta[property="og:image"]')["content"]
        self.works[rank]["opengraph_creator_image_url"] = og_image_url

        # head > meta property="og:description"
        creator_description = soup.select_one('meta[property="og:description"]')["content"]
        self.works[rank]["opengraph_creator_description"] = creator_description

    def get_opengraphs(self):
        for rank in self.works:
            time.sleep(2)
            self.get_work_opengraph(rank, self.works[rank]["work_url"])
            time.sleep(2)
            self.get_creator_opengraph(rank, self.works[rank]["creator_url"])

    def save_as_json(self):
        with open("data/daily_illust_rankings.json", "w") as f:
            json.dump({"timestamp": self.timestamp, **self.works}, f, indent=4)

if __name__ == "__main__":
    # for test
    ranking = DailyIllustRankings()
    ranking.get_work_urls_from_ranking()
    ranking.get_opengraphs()
    ranking.save_as_json()
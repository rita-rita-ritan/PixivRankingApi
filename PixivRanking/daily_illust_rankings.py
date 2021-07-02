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

        creator_names = [creator_name.get_text() for creator_name
                        in soup.select(".user-name") if creator_name.get_text()]
        creator_urls = ["https://www.pixiv.net" + creator_relative_url["href"] 
                        for creator_relative_url in soup.select(".user-container") 
                        if creator_relative_url["href"]]
        work_titles = [work_title.get_text() for work_title 
                        in soup.select(".title") if work_title.get_text()]
        work_urls = ["https://www.pixiv.net" + work_relative_url["href"] 
                        for work_relative_url in soup.select(".work")
                        if work_relative_url["href"]]
        
        if len(creator_names) == len(creator_urls) == len(work_titles) == len(work_urls):
            for i in range(self.len_works):
                self.works[i + 1]["creator_name"] = creator_names[i]
                self.works[i + 1]["creator_url"] = creator_urls[i]
                self.works[i + 1]["work_title"] = work_titles[i]
                self.works[i + 1]["work_url"] = work_urls[i]
        else:
            print("error: Failed to get the ranking information.")
            for i in range(self.len_works):
                self.works[i + 1]["creator_name"] = "うまく準備できなかったようです……(ノω・、`) ｺﾞﾒﾝ"
                self.works[i + 1]["creator_url"] = ""
                self.works[i + 1]["work_title"] = "うまく準備できなかったようです……(ノω・、`) ｺﾞﾒﾝ"
                self.works[i + 1]["work_url"] = ""

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
        time.sleep(1)
        try:
            response = requests.get(og_image_url)
            response.raise_for_status()
            print(f"{rank}/{self.len_works}: {response.status_code}")
            self.works[rank]["opengraph_creator_image_url"] = og_image_url
        except requests.exceptions.RequestException as e:
            print(f"{rank}/{self.len_works}: Cannot get creator image: ",e)
            self.works[rank]["opengraph_creator_image_url"] = ""
        

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
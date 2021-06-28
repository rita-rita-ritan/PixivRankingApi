import requests
from bs4 import BeautifulSoup
import json
import schedule
import time

def scraping():
    source_html = requests.get('https://www.pixiv.net/ranking.php?mode=daily&content=illust')
    soup = BeautifulSoup(source_html.text, "html.parser")
    works = [
        {
            "rank": i + 1,
            "href": "https://www.pixiv.net" + v["href"]
        } for i, v in enumerate(soup.select(".work"))
    ]

    with open("data/daily-illust-ranking.json", "w") as f:
        json.dump(works, f, indent=4)

if __name__ == "__main__":
    schedule.every().day.at("0:00").do(scraping)

    while True:
        schedule.run_pending()
        time.sleep(100)
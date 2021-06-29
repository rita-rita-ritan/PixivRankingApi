import schedule
import time

from .daily_illust_rankings import DailyIllustRankings

def update():
    rankings = DailyIllustRankings()
    rankings.get_work_urls_from_ranking()
    rankings.get_opengraphs()
    rankings.save_as_json()

if __name__ == "__main__":
    schedule.every().day.at("12:00").do(update)

    while True:
        schedule.run_pending()
        time.sleep(100)
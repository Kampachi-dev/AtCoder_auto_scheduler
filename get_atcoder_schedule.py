from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup


def get_atcoder_schedule():
    "AtCoder のコンテスト一覧ページから今後のコンテストの開催情報を取得する"

    url = "https://atcoder.jp/contests"
    params = {"lang": "ja"}

    response = requests.get(url, params=params)
    print(response.status_code)
    bs = BeautifulSoup(response.text, "html.parser")
    print(bs)
    contest_table_upcoming = bs.find("div", attrs={"id": "contest-table-upcoming"})
    print(contest_table_upcoming)
    if contest_table_upcoming is None:
        raise ValueError("'contest_table_upcoming' is None")
    upcomings = contest_table_upcoming.find("tbody")
    if upcomings is None:
        raise ValueError("'upcomings' is None")

    contests = {}
    for contest in upcomings.find_all("tr"):
        contest_data = []
        for data in contest.find_all("td"):
            contest_data.append(data)

        s = contest_data[0].find("time").getText()
        start_at = datetime.strptime(s, "%Y-%m-%d %H:%M:%S+0900")

        contest_type = contest_data[1].find("span").get("title")
        contest_url = "https://atcoder.jp" + contest_data[1].find("a").get("href")
        common_title = contest_url.split('/')[-1].upper()
        official_title = contest_data[1].find("a").getText()

        h, m = map(int, contest_data[2].getText().split(':'))
        duration = timedelta(hours=h, minutes=m)
        end_at = start_at + duration

        contests[common_title] = {
            "official_title": official_title,
            "type": contest_type,
            "url": contest_url,
            "start_at": start_at.isoformat(),
            "end_at": end_at.isoformat()
        }

    return contests


if __name__ == "__main__":
    contests = get_atcoder_schedule()
    print(contests)

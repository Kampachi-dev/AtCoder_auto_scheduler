import json
from get_atcoder_schedule import get_atcoder_schedule
from edit_calendar import create_events, update_events


def main():

    contests = get_atcoder_schedule()

    with open("contests.json") as f:
        contests_local = json.load(f)

    for contest in contests:

        # とりあえずアルゴに絞って登録する
        if contests[contest]["type"] != "Algorithm":
            continue

        if contest not in contests_local:
            # 新規登録
            event_id = create_events(title=contest,
                                     start_at=contests[contest]["start_at"],
                                     end_at=contests[contest]["end_at"],
                                     event_url=contests[contest]["url"],
                                     official_title=contests[contest]["official_title"])
            contests_local[contest] = {
                "official_title": contests[contest]["official_title"],
                "type": contests[contest]["type"],
                "url": contests[contest]["url"],
                "start_at": contests[contest]["start_at"],
                "end_at": contests[contest]["end_at"],
                "event_id": event_id
            }

        else:
            # 開始時刻と終了時刻のどちらも変更されていなければ、なにもしない
            # 変更があれば更新する
            if contests[contest]["start_at"] == contests_local[contest]["start_at"] \
                    and contests[contest]["end_at"] == contests_local[contest]["end_at"]:
                pass
            else:
                update_events(event_id=contests_local[contest]["event_id"],
                              title=contest,
                              official_title=contests[contest]["official_title"],
                              start_at=contests[contest]["start_at"],
                              end_at=contests[contest]["end_at"])
                contests_local[contest]["official_title"] = contests[contest]["official_title"]
                contests_local[contest]["start_at"] = contests[contest]["start_at"]
                contests_local[contest]["end_at"] = contests[contest]["end_at"]

    with open("contests.json", "w") as f:
        json.dump(contests_local, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()

import os
import requests
import json

ACCESS_TOKEN = os.environ["TIMETREE_ACCESS_TOKEN"]
CALENDAR_ID = os.environ["TIMETREE_CALENDAR_ID"]


def select_label_id(title: str) -> int:
    label_id = 10
    title_prefix = title[:3]
    if title_prefix == "ABC":
        label_id = 1
    if title_prefix == "ARC":
        label_id = 2
    if title_prefix == "AGC":
        label_id = 3
    return label_id


def create_events(title: str, start_at: str, end_at: str, event_url: str, official_title: str) -> str:
    "カレンダーに予定を新規登録する"

    # ヘッダーの設定
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/vnd.timetree.v1+json",
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }
    url = f"https://timetreeapis.com/calendars/{CALENDAR_ID}/events"
    label_id = select_label_id(title=title)

    event = {
        "data": {
            "attributes": {
                "category": "schedule",
                "title": title,
                "all_day": False,
                "start_at": start_at,
                "start_timezone": "Asia/Tokyo",
                "end_at": end_at,
                "end_timezone": "Asia/Tokyo",
                "url": event_url,
                "description": official_title,
            },
            "relationships": {
                "label": {
                    "data": {
                        "id": f"{CALENDAR_ID},{label_id}",
                        "type": "label"
                    }
                },
                "attendees": {
                    "data": [
                        {"id": f"{CALENDAR_ID},5772846303807810", "type": "user"}
                    ]
                }
            }
        }
    }

    response = requests.post(url, headers=headers, data=json.dumps(event))
    data = response.json()
    event_id = data["data"]["id"]
    return event_id


def update_events(event_id: str, title: str, official_title: str, start_at: str, end_at: str) -> None:
    "カレンダーに登録されている予定を更新する"

    # ヘッダーの設定
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/vnd.timetree.v1+json",
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }
    url = f"https://timetreeapis.com/calendars/{CALENDAR_ID}/events/{event_id}"
    label_id = select_label_id(title)

    event = {
        "data": {
            "attributes": {
                "category": "schedule",
                "title": title,
                "all_day": False,
                "start_at": start_at,
                "start_timezone": "Asia/Tokyo",
                "end_at": end_at,
                "end_timezone": "Asia/Tokyo",
                "description": official_title
            },
            "relationships": {
                "label": {
                    "data": {
                        "id": f"{CALENDAR_ID},{label_id}",
                        "type": "label"
                    }
                },
                "attendees": {
                    "data": [
                        {"id": f"{CALENDAR_ID},8533784680695705", "type": "user"}
                    ]
                }
            }
        }
    }

    requests.put(url, headers=headers, data=json.dumps(event))

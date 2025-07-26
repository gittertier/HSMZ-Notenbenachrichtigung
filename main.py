import json
import os
import pickle

import requests

from gradeUtils import get_grades
from loginRequests import login_session

session = requests.session()
session.headers.update(
    {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:139.0) Gecko/20100101 Firefox/139.0"
    }
)


def load_config(config_path="config.json"):
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)
    return config


config = load_config()
username = config["username"]
password = config["password"]
COOKIE_FILE = config["COOKIE_FILE"]
GRADES_FILE = config["GRADES_FILE"]
DISCORD_WEBHOOK_URL = config["DISCORD_WEBHOOK_URL"]


def setup_session():
    if os.path.exists(COOKIE_FILE):
        with open(COOKIE_FILE, "rb") as f:
            cookies = pickle.load(f)
            session.cookies.update(cookies)


def persist_session():
    with open(COOKIE_FILE, "wb") as f:
        pickle.dump(session.cookies, f)


def write_grades_to_file(grades):
    with open(GRADES_FILE, "w", encoding="utf-8") as f:
        for grade in grades:
            f.write(grade + "\n")


def load_previous_grades():
    if not os.path.exists(GRADES_FILE):
        return set()
    with open(GRADES_FILE, "r", encoding="utf-8") as f:
        return set(line.strip() for line in f)


def send_discord_webhook(new_grades):
    embed = {
        "title": "📋 New Grades Detected",
        "description": "\n".join(f"- {g}" for g in new_grades),
        "color": 0x5CDBF0,  # You can pick any hex color
    }
    payload = {"embeds": [embed]}
    requests.post(DISCORD_WEBHOOK_URL, json=payload)


def main():

    setup_session()

    try:
        grades = get_grades(session)
    except Exception as e:
        print("new session required")
        if str(e) != "unauthenticated":
            exit()
        login_session(session, username, password)
        grades = get_grades(session)

    previous_grades = load_previous_grades()
    new_grades = [g for g in grades if g not in previous_grades]

    if new_grades:
        send_discord_webhook(new_grades)

    write_grades_to_file(grades)

    persist_session()


if __name__ == "__main__":
    main()

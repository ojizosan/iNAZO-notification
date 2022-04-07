import re
import requests
from bs4 import BeautifulSoup
import sqlite3
import json

import settings


def fetch_html(url):
    """
    Args:
        url -> string

    Return:
        html -> string
    """
    try:
        res = requests.get(url)
        res.raise_for_status()
    except requests.exceptions.HTTPError as e:
        error(f"fetch_html() error: {e}")

    return res.text


# TODO: parser errorに対応
def get_year_terms(html):
    """
    Args:
        html -> string

    Return:
        year_term_list -> List[(year: int, term: int)]
    """
    soup = BeautifulSoup(html, "html.parser")

    options = [
        o.text
        for o in soup.find("select", id="ddlTerm").find_all("option")
        if o.text != "---------------"
    ]

    results = [tuple(map(int, re.findall(r"\d+", o))) for o in options]
    return results


def insert_year_term(year_term):
    """
    Args:
        year_term -> (year: int, term: int)
    """

    conn = sqlite3.connect(settings.DB_NAME)
    cur = conn.cursor()
    cur.execute("INSERT INTO gradeterm (year, term) VALUES (?, ?)", year_term)

    conn.commit()

    cur.close()
    conn.close()


def fetch_latest_year_term():
    """
    Return:
        (year: int, term: int)
    """

    conn = sqlite3.connect(settings.DB_NAME)
    cur = conn.cursor()

    res = cur.execute(
        "SELECT year, term FROM gradeterm ORDER BY year DESC, term DESC LIMIT 1"
    ).fetchall()

    # len(res)は0か1
    if len(res) == 0:
        raise Exception("初期データが登録されていません。")

    cur.close()
    conn.close()

    return res[0]


def push_slack_webhook(message):
    """
    slackのwebhookにpushする。エラーが飽きた場合はログを残して強制終了。

    Args:
        message -> string
    """
    payload = {"text": message}
    try:
        res = requests.post(settings.SLACK_WEBHOOK_URL, data=json.dumps(payload))
        res.raise_for_status()
    except Exception as e:
        print(f"push_slack_webhook() error: {e}")
        exit(1)


def is_new_term(year_term):
    """
    Args:
        year_term -> (year: int, term: int)

    Return:
        is_new :bool
    """

    db_year_term = fetch_latest_year_term()
    if year_term[0] > db_year_term[0]:
        return True
    elif year_term[0] < db_year_term[0]:
        return False
    else:
        return year_term[1] > db_year_term[1]


def get_latest_year_term(year_term_list):
    """
    Args:
        year_term_list -> List[(year: int, term: int)]

    Return:
        year_term -> (year: int, term: int)
    """

    if len(year_term_list) == 0:
        raise Exception("get_latest_year_term() error: データが空です")

    year_term_list.sort(reverse=True)

    return year_term_list[0]


def error(message):
    print(message)
    push_slack_webhook(message)
    exit(1)

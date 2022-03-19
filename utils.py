import bs4
import requests
import sqlite3
import json

import settings

def get_html(url):
    r = requests.get(url)
    return r.text


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

    res = cur.execute("SELECT year, term FROM gradeterm ORDER BY year DESC, term DESC LIMIT 1").fetchall()

    # len(res)は0か1    
    if len(res) == 0:
        raise Exception("初期データが登録されていません。")

    cur.close()
    conn.close()

    return res[0]

def push_slack_webhook(message):
    """
    Args:
        message -> string
    """
    payload = {
        "text": message
    }
    try:
        res = requests.post(settings.SLACK_WEBHOOK_URL, data=json.dumps(payload))
        res.raise_for_status()
    except requests.exceptions.HTTPError as e:
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

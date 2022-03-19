import bs4
import requests
import sqlite3

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
import sqlite3
from logging import getLogger

from src import settings
from src.utils import fetch_html, get_latest_year_term, get_year_terms, insert_year_term

logger = getLogger(__name__)


def main():
    conn = sqlite3.connect(settings.DB_NAME)

    cur = conn.cursor()

    try:
        cur.execute(
            """
        CREATE TABLE gradeterm (
            year INTEGER NOT NULL,
            term INTEGER NOT NULL,
            created_at TEXT NOT NULL DEFAULT (DATETIME('now', 'localtime')),
            PRIMARY KEY(year, term)
        )
        """
        )
    except sqlite3.OperationalError as e:
        # 既に登録済みの場合など
        logger.error(f"message: {e}")
        conn.close()
        exit(1)

    # 初期データの登録
    html = fetch_html(settings.HOKUDAI_GRADE_URL)
    year_terms = get_year_terms(html)
    now_latest = get_latest_year_term(year_terms)
    insert_year_term(now_latest)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()

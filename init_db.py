import sqlite3
import settings


def main():
    conn = sqlite3.connect(settings.DB_NAME)

    cur = conn.cursor()

    try:
        cur.execute("""
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
        print(f"message: {e}")
        conn.close()
        exit(1)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()

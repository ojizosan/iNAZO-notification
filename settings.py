import os
from dotenv import load_dotenv


# .envの読み込み
load_dotenv()

DB_NAME = "sqlite3.db"
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
HOKUDAI_GRADE_URL = "http://educate.academic.hokudai.ac.jp/seiseki/GradeDistSerch.aspx"

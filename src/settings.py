import os
from logging import config
from urllib.parse import urlparse

from dotenv import load_dotenv

from src.log import SlackFilter

# .envの読み込み
load_dotenv()

DB_NAME = "sqlite3.db"
SLACK_WEBHOOK_URL = urlparse(os.getenv("SLACK_WEBHOOK_URL"))
HOKUDAI_GRADE_URL = "http://educate.academic.hokudai.ac.jp/seiseki/GradeDistSerch.aspx"
DEBUG = os.getenv("DEBUG", "False") == "True"
LOGPATH = os.getenv("LOGPATH", "test.log")

LOGGING_LOCAL = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "standard": {
            "format": "%(asctime)s {%(filename)s:%(lineno)d} [%(levelname)s] - %(message)s"
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "formatter": "standard",
            "class": "logging.StreamHandler",
        }
    },
    "loggers": {
        "src": {
            "handlers": ["console"],
            "level": "DEBUG",
        },
    },
}

LOGGING_PRODUCT = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "standard": {
            "format": "%(asctime)s {%(filename)s:%(lineno)d} [%(levelname)s] - %(message)s"
        },
    },
    "filters": {"slack_filter": {"()": SlackFilter}},
    "handlers": {
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": LOGPATH,
            "formatter": "standard",
        },
        "slack": {
            "level": "INFO",
            "formatter": "standard",
            "class": "src.log.SlackHandler",
            "host": SLACK_WEBHOOK_URL.netloc,
            "url": SLACK_WEBHOOK_URL.path,
            "method": "POST",
            "secure": True,
            "filters": ["slack_filter"],
        },
    },
    "loggers": {
        "src": {
            "handlers": ["file", "slack"],
            "level": "INFO",
        },
    },
}

if DEBUG:
    config.dictConfig(LOGGING_LOCAL)
else:
    config.dictConfig(LOGGING_PRODUCT)

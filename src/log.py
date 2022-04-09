import logging
from logging.handlers import HTTPHandler


class SlackHandler(HTTPHandler):
    def mapLogRecord(self, record):
        text = self.format(record)
        return {"payload": {"text": text}}


class SlackFilter(logging.Filter):
    def filter(self, record):
        info_levelno = 20
        # warning以上でslackに通知する
        if record.levelno > info_levelno:
            return True

        return getattr(record, "notify_slack", False)

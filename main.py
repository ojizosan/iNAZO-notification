from logging import getLogger

from src import settings
from src.utils import (
    fetch_html,
    get_latest_year_term,
    get_year_terms,
    insert_year_term,
    is_new_term,
)

# __name__では__main__になるので、直接srcを指定する。
logger = getLogger("src")


def main():
    try:
        html = fetch_html(settings.HOKUDAI_GRADE_URL)
    except Exception as e:
        logger.error(f"fetch_html() failure: {e}")
        exit(1)

    year_terms = get_year_terms(html)
    now_latest = get_latest_year_term(year_terms)

    isNew = None
    try:
        isNew = is_new_term(now_latest)
    except Exception as e:
        logger.error(f"is_new_term() failure: {e}")
        exit(1)

    if isNew:
        try:
            insert_year_term(now_latest)
        except Exception as e:
            logger.error(f"insert_year_term() failure: {e}")
            exit(1)

        logger.info("新たな成績が公開されました。", extra={"notify_slack": True})
    else:
        logger.info("成績は更新されていません。")


if __name__ == "__main__":
    main()

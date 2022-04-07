import settings
from utils import (
    fetch_html,
    get_year_terms,
    insert_year_term,
    push_slack_webhook,
    is_new_term,
    get_latest_year_term,
    error,
)


def main():
    try:
        html = fetch_html(settings.HOKUDAI_GRADE_URL)
    except Exception as e:
        error(f"fetch_html() failure: {e}")

    year_terms = get_year_terms(html)
    now_latest = get_latest_year_term(year_terms)

    isNew = None
    try:
        isNew = is_new_term(now_latest)
    except Exception as e:
        error(f"is_new_term() failure: {e}")

    if isNew:
        try:
            insert_year_term(now_latest)
        except Exception as e:
            error(f"insert_year_term() failure: {e}")

        push_slack_webhook("新たな成績が公開されました。")
    else:
        # TODO: 更新されていない時にslackへ通知するかどうかの仕様を検討
        print("not new grade.")


if __name__ == "__main__":
    main()

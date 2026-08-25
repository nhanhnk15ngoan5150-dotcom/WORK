import re
import sqlite3
from calendar import monthrange
from datetime import datetime, timedelta
from pathlib import Path


# 1. 配置数据库路径
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DB_FILE = BASE_DIR / "data" / "moneki.db"


# 2. 获取数据库日期范围
def get_data_date_range():
    conn = sqlite3.connect(
        DB_FILE
    )

    cursor = conn.cursor()

    result = cursor.execute(
        """
        SELECT
            MIN(date),
            MAX(date)
        FROM sales
        """
    ).fetchone()

    conn.close()

    return {
        "min_date": result[0],
        "max_date": result[1],
    }


# 3. 获取下个月月初
def _next_month_start(
    date_value: datetime
):
    if date_value.month == 12:
        return datetime(
            date_value.year + 1,
            1,
            1
        )

    return datetime(
        date_value.year,
        date_value.month + 1,
        1
    )


# 4. 获取上个月月初
def _previous_month_start(
    date_value: datetime
):
    if date_value.month == 1:
        return datetime(
            date_value.year - 1,
            12,
            1
        )

    return datetime(
        date_value.year,
        date_value.month - 1,
        1
    )


# 5. 判断月份是否与数据库范围重叠
def _month_has_data(
    start_date: datetime,
    end_date: datetime,
    min_date: datetime,
    max_date: datetime
):
    return (
        end_date > min_date
        and start_date <= max_date
    )


# 6. 查找数据库范围内最近匹配年份
def _find_available_month(
    month: int,
    min_date: datetime,
    max_date: datetime
):
    candidates = []

    for year in range(
        min_date.year,
        max_date.year + 1
    ):
        start_date = datetime(
            year,
            month,
            1
        )

        end_date = _next_month_start(
            start_date
        )

        if _month_has_data(
            start_date,
            end_date,
            min_date,
            max_date
        ):
            candidates.append(
                {
                    "year": year,
                    "start_date": start_date,
                    "end_date": end_date,
                }
            )

    if not candidates:
        return None

    return candidates[-1]


# 7. 构造超出数据范围结果
def _build_out_of_range_result(
    start_date: datetime,
    end_date: datetime,
    min_date: datetime,
    max_date: datetime
):
    return {
        "start_date": start_date.strftime(
            "%Y-%m-%d"
        ),
        "end_date": end_date.strftime(
            "%Y-%m-%d"
        ),
        "available_start": min_date.strftime(
            "%Y-%m-%d"
        ),
        "available_end": max_date.strftime(
            "%Y-%m-%d"
        ),
        "mode": "out_of_range",
    }


# 8. 解析用户时间表达
def parse_time_expression(
    time_expression: str | None
):
    date_range = get_data_date_range()

    if (
        not date_range.get("min_date")
        or not date_range.get("max_date")
    ):
        return {
            "mode": "unknown"
        }

    min_date = datetime.strptime(
        date_range["min_date"],
        "%Y-%m-%d"
    )

    max_date = datetime.strptime(
        date_range["max_date"],
        "%Y-%m-%d"
    )

    # 9. 未指定时间时使用全部真实数据
    if not time_expression:
        end_date = (
            max_date
            + timedelta(days=1)
        )

        return {
            "start_date": min_date.strftime(
                "%Y-%m-%d"
            ),
            "end_date": end_date.strftime(
                "%Y-%m-%d"
            ),
            "mode": "all",
        }

    expression = (
        str(time_expression)
        .strip()
        .replace(" ", "")
    )

    # 10. 月份语言映射
    month_map = {
        "一月": 1,
        "1月": 1,
        "二月": 2,
        "2月": 2,
        "三月": 3,
        "3月": 3,
        "四月": 4,
        "4月": 4,
        "五月": 5,
        "5月": 5,
        "六月": 6,
        "6月": 6,
        "七月": 7,
        "7月": 7,
        "八月": 8,
        "8月": 8,
        "九月": 9,
        "9月": 9,
        "十月": 10,
        "10月": 10,
        "十一月": 11,
        "11月": 11,
        "十二月": 12,
        "12月": 12,
    }

    # 11. 解析明确年份 + 月份
    year_month_match = re.fullmatch(
        r"(\d{4})年(.+)",
        expression
    )

    if year_month_match:
        year = int(
            year_month_match.group(1)
        )

        month_text = (
            year_month_match.group(2)
        )

        month = month_map.get(
            month_text
        )

        if month is None:
            return {
                "mode": "unknown"
            }

        start_date = datetime(
            year,
            month,
            1
        )

        end_date = _next_month_start(
            start_date
        )

        if not _month_has_data(
            start_date,
            end_date,
            min_date,
            max_date
        ):
            return _build_out_of_range_result(
                start_date,
                end_date,
                min_date,
                max_date
            )

        return {
            "start_date": start_date.strftime(
                "%Y-%m-%d"
            ),
            "end_date": end_date.strftime(
                "%Y-%m-%d"
            ),
            "mode": "month",
        }

    # 12. 解析不带年份的月份
    if expression in month_map:
        month = month_map[
            expression
        ]

        available_month = (
            _find_available_month(
                month,
                min_date,
                max_date
            )
        )

        # 数据库存在这个月份
        if available_month:
            return {
                "start_date": (
                    available_month[
                        "start_date"
                    ].strftime(
                        "%Y-%m-%d"
                    )
                ),
                "end_date": (
                    available_month[
                        "end_date"
                    ].strftime(
                        "%Y-%m-%d"
                    )
                ),
                "mode": "month",
            }

        # 数据库不存在这个月份
        fallback_start = datetime(
            max_date.year,
            month,
            1
        )

        fallback_end = _next_month_start(
            fallback_start
        )

        return _build_out_of_range_result(
            fallback_start,
            fallback_end,
            min_date,
            max_date
        )

    # 13. 最近表示数据库最新完整月份与上一月份
    if expression == "最近":
        latest_month_start = datetime(
            max_date.year,
            max_date.month,
            1
        )

        last_day = monthrange(
            max_date.year,
            max_date.month
        )[1]

        # 最新月份完整
        if max_date.day == last_day:
            current_start = (
                latest_month_start
            )

        # 最新月份不完整时使用上一个完整月
        else:
            current_start = (
                _previous_month_start(
                    latest_month_start
                )
            )

        current_end = _next_month_start(
            current_start
        )

        previous_start = (
            _previous_month_start(
                current_start
            )
        )

        return {
            "current_start": (
                current_start.strftime(
                    "%Y-%m-%d"
                )
            ),
            "current_end": (
                current_end.strftime(
                    "%Y-%m-%d"
                )
            ),
            "previous_start": (
                previous_start.strftime(
                    "%Y-%m-%d"
                )
            ),
            "previous_end": (
                current_start.strftime(
                    "%Y-%m-%d"
                )
            ),
            "mode": "compare",
        }

    # 14. 无法识别时间
    return {
        "mode": "unknown",
    }
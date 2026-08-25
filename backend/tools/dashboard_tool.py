from datetime import date, datetime
from pathlib import Path
import sqlite3

from tools.sales_tool import get_sales_summary
from tools.store_tool import get_store_category_sales


# 1. 配置数据库路径
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DB_FILE = BASE_DIR / "data" / "moneki.db"


# 2. 月份偏移
def add_months(
    month_start: date,
    offset: int,
):
    month_index = (
        month_start.year * 12
        + month_start.month
        - 1
        + offset
    )

    year = month_index // 12
    month = month_index % 12 + 1

    return date(
        year,
        month,
        1,
    )


# 3. 查询数据库最新销售日期
def get_latest_sales_date():
    conn = sqlite3.connect(DB_FILE)

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT MAX(date)
        FROM sales
        """
    )

    result = cursor.fetchone()

    conn.close()

    if (
        not result
        or not result[0]
    ):
        return None

    return result[0]


# 4. 计算变化率
def calculate_change_rate(
    current_value,
    previous_value,
):
    if (
        previous_value is None
        or previous_value == 0
        or current_value is None
    ):
        return None

    return round(
        (
            current_value
            - previous_value
        )
        / previous_value
        * 100,
        2,
    )


# 5. 查询 Dashboard 真实经营数据
def get_dashboard_data():
    latest_date_text = (
        get_latest_sales_date()
    )

    if not latest_date_text:
        return {
            "success": False,
            "message": "没有查询到经营数据",
        }

    latest_date = datetime.strptime(
        latest_date_text,
        "%Y-%m-%d",
    ).date()

    latest_month_start = date(
        latest_date.year,
        latest_date.month,
        1,
    )

    next_month_start = add_months(
        latest_month_start,
        1,
    )

    previous_month_start = add_months(
        latest_month_start,
        -1,
    )


    # 6. 查询最新月和上月经营指标
    current = get_sales_summary(
        latest_month_start.isoformat(),
        next_month_start.isoformat(),
    )

    previous = get_sales_summary(
        previous_month_start.isoformat(),
        latest_month_start.isoformat(),
    )

    if not current["success"]:
        return {
            "success": False,
            "message": "最新周期经营数据查询失败",
        }


    # 7. 查询最新月门店品类
    category_result = (
        get_store_category_sales(
            latest_month_start.isoformat(),
            next_month_start.isoformat(),
        )
    )

    if category_result["success"]:
        top_category = (
            category_result["top_category"]
        )
    else:
        top_category = None


    # 8. 生成最近三个月趋势
    trend = []

    for offset in (-2, -1, 0):
        month_start = add_months(
            latest_month_start,
            offset,
        )

        month_end = add_months(
            month_start,
            1,
        )

        summary = get_sales_summary(
            month_start.isoformat(),
            month_end.isoformat(),
        )

        if not summary["success"]:
            continue

        trend.append(
            {
                "month": (
                    f"{month_start.year}-"
                    f"{month_start.month:02d}"
                ),
                "label": (
                    f"{month_start.month}月"
                ),
                "total_sales": (
                    summary["total_sales"]
                ),
                "order_count": (
                    summary["order_count"]
                ),
                "avg_order_value": (
                    summary["avg_order_value"]
                ),
            }
        )


    # 9. 计算环比变化
    sales_change_rate = None
    order_change_rate = None
    aov_change_rate = None

    if previous["success"]:
        sales_change_rate = (
            calculate_change_rate(
                current["total_sales"],
                previous["total_sales"],
            )
        )

        order_change_rate = (
            calculate_change_rate(
                current["order_count"],
                previous["order_count"],
            )
        )

        aov_change_rate = (
            calculate_change_rate(
                current["avg_order_value"],
                previous["avg_order_value"],
            )
        )


    # 10. 返回 Dashboard 数据
    return {
        "success": True,
        "latest_data_date": latest_date_text,
        "period": {
            "year": latest_month_start.year,
            "month": latest_month_start.month,
            "label": (
                f"{latest_month_start.year}年"
                f"{latest_month_start.month}月"
            ),
        },
        "summary": {
            "total_sales": (
                current["total_sales"]
            ),
            "order_count": (
                current["order_count"]
            ),
            "avg_order_value": (
                current["avg_order_value"]
            ),
            "sales_change_rate": (
                sales_change_rate
            ),
            "order_change_rate": (
                order_change_rate
            ),
            "aov_change_rate": (
                aov_change_rate
            ),
            "top_category": (
                top_category["category"]
                if top_category
                else None
            ),
            "top_category_sales": (
                top_category["total_sales"]
                if top_category
                else None
            ),
        },
        "trend": trend,
        "message": "查询成功",
    }
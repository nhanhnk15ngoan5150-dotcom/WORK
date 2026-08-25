from contextlib import closing
from datetime import date, datetime
from pathlib import Path
import sqlite3


# 1. 配置数据库路径
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DB_FILE = BASE_DIR / "data" / "moneki.db"


def _add_months(
    month_start: date,
    offset: int,
):
    """返回相对 month_start 偏移后的月份首日。"""
    month_index = (
        month_start.year * 12
        + month_start.month
        - 1
        + offset
    )

    return date(
        month_index // 12,
        month_index % 12 + 1,
        1,
    )


def _query_store_metrics(
    connection: sqlite3.Connection,
    start_date: str,
    end_date: str,
):
    """按门店查询一个时间段的经营指标，并保留零销售门店。"""
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT
            st.store_id,
            st.store_name,
            st.category,
            st.district,
            ROUND(COALESCE(SUM(s.amount), 0), 2) AS total_sales,
            COUNT(DISTINCT s.order_id) AS order_count,
            COALESCE(SUM(s.qty), 0) AS total_quantity
        FROM stores st
        LEFT JOIN sales s
            ON s.store_id = st.store_id
           AND s.date >= ?
           AND s.date < ?
        GROUP BY
            st.store_id,
            st.store_name,
            st.category,
            st.district
        ORDER BY total_sales DESC, st.store_id ASC
        """,
        (
            start_date,
            end_date,
        ),
    )

    rows = cursor.fetchall()
    period_sales = round(
        sum(float(row[4] or 0) for row in rows),
        2,
    )

    stores = []

    for index, row in enumerate(rows):
        total_sales = round(float(row[4] or 0), 2)
        order_count = int(row[5] or 0)
        total_quantity = int(row[6] or 0)

        stores.append(
            {
                "rank": index + 1,
                "store_id": row[0],
                "store_name": row[1],
                "category": row[2],
                "district": row[3],
                "total_sales": total_sales,
                "order_count": order_count,
                "avg_order_value": (
                    round(total_sales / order_count, 2)
                    if order_count
                    else None
                ),
                "total_quantity": total_quantity,
                "sales_share": (
                    round(total_sales / period_sales * 100, 2)
                    if period_sales
                    else 0.0
                ),
            }
        )

    return stores


def _query_distinct_order_count(
    connection: sqlite3.Connection,
    start_date: str,
    end_date: str,
):
    """查询一个时间段内不重复的订单数。"""
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT COUNT(DISTINCT order_id)
        FROM sales
        WHERE date >= ?
          AND date < ?
        """,
        (
            start_date,
            end_date,
        ),
    )

    row = cursor.fetchone()

    return int(row[0] or 0) if row else 0


# 2. 查询门店页面所需的真实聚合数据

def get_store_dashboard_data(
    db_file: str | Path = DB_FILE,
):
    database_path = Path(db_file)

    if not database_path.exists():
        return {
            "success": False,
            "message": "门店数据库不存在",
        }

    try:
        with closing(sqlite3.connect(database_path)) as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT MAX(date)
                FROM sales
                """
            )
            latest_result = cursor.fetchone()
            latest_date_text = (
                latest_result[0]
                if latest_result
                else None
            )

            if not latest_date_text:
                return {
                    "success": False,
                    "message": "没有查询到门店经营数据",
                }

            latest_date = datetime.strptime(
                latest_date_text,
                "%Y-%m-%d",
            ).date()
            current_month_start = date(
                latest_date.year,
                latest_date.month,
                1,
            )
            next_month_start = _add_months(
                current_month_start,
                1,
            )

            ranking = _query_store_metrics(
                connection,
                current_month_start.isoformat(),
                next_month_start.isoformat(),
            )
            current_order_count = _query_distinct_order_count(
                connection,
                current_month_start.isoformat(),
                next_month_start.isoformat(),
            )

            if not ranking:
                return {
                    "success": False,
                    "message": "没有查询到门店资料",
                }

            trend = []

            for offset in (-2, -1, 0):
                month_start = _add_months(
                    current_month_start,
                    offset,
                )
                month_end = _add_months(
                    month_start,
                    1,
                )
                month_stores = _query_store_metrics(
                    connection,
                    month_start.isoformat(),
                    month_end.isoformat(),
                )
                month_order_count = _query_distinct_order_count(
                    connection,
                    month_start.isoformat(),
                    month_end.isoformat(),
                )

                trend.append(
                    {
                        "month": (
                            f"{month_start.year}-"
                            f"{month_start.month:02d}"
                        ),
                        "label": f"{month_start.month}月",
                        "total_sales": round(
                            sum(
                                item["total_sales"]
                                for item in month_stores
                            ),
                            2,
                        ),
                        "order_count": month_order_count,
                        "total_quantity": sum(
                            item["total_quantity"]
                            for item in month_stores
                        ),
                        "stores": month_stores,
                    }
                )

    except (sqlite3.Error, ValueError):
        return {
            "success": False,
            "message": "门店数据查询失败",
        }

    total_sales = round(
        sum(item["total_sales"] for item in ranking),
        2,
    )
    order_count = current_order_count
    total_quantity = sum(
        item["total_quantity"] for item in ranking
    )
    active_stores = sum(
        1 for item in ranking
        if item["order_count"] > 0
    )
    top_store = next(
        (
            item for item in ranking
            if item["total_sales"] > 0
        ),
        None,
    )

    store_options = [
        {
            "store_id": item["store_id"],
            "store_name": item["store_name"],
        }
        for item in sorted(
            ranking,
            key=lambda item: item["store_id"],
        )
    ]

    return {
        "success": True,
        "latest_data_date": latest_date_text,
        "period": {
            "year": current_month_start.year,
            "month": current_month_start.month,
            "label": (
                f"{current_month_start.year}年"
                f"{current_month_start.month}月"
            ),
            "start_date": current_month_start.isoformat(),
            "end_date": next_month_start.isoformat(),
        },
        "summary": {
            "total_stores": len(ranking),
            "active_stores": active_stores,
            "total_sales": total_sales,
            "order_count": order_count,
            "avg_order_value": (
                round(total_sales / order_count, 2)
                if order_count
                else None
            ),
            "avg_store_sales": (
                round(total_sales / active_stores, 2)
                if active_stores
                else None
            ),
            "total_quantity": total_quantity,
            "top_store": top_store,
        },
        "filters": {
            "stores": store_options,
            "categories": sorted(
                {
                    item["category"]
                    for item in ranking
                    if item["category"]
                }
            ),
            "districts": sorted(
                {
                    item["district"]
                    for item in ranking
                    if item["district"]
                }
            ),
        },
        "ranking": ranking,
        "trend": trend,
        "message": "查询成功",
    }

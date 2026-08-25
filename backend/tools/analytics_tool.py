from contextlib import closing
from datetime import date, datetime
from pathlib import Path
import sqlite3


BASE_DIR = Path(__file__).resolve().parent.parent.parent
DB_FILE = BASE_DIR / "data" / "moneki.db"


def _add_months(
    month_start: date,
    offset: int,
):
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



def _calculate_change_rate(
    current_value,
    previous_value,
):
    if previous_value in (None, 0) or current_value is None:
        return None

    return round(
        (current_value - previous_value)
        / previous_value
        * 100,
        2,
    )
def _build_filter_clause(
    start_date: str,
    end_date: str,
    store_id: str | None,
    category: str | None,
    product_id: str | None,
):
    conditions = [
        "s.date >= ?",
        "s.date < ?",
    ]
    parameters = [
        start_date,
        end_date,
    ]

    if store_id:
        conditions.append("s.store_id = ?")
        parameters.append(store_id)

    if category:
        conditions.append("st.category = ?")
        parameters.append(category)

    if product_id:
        conditions.append("s.product_id = ?")
        parameters.append(product_id)

    return (
        " AND ".join(conditions),
        parameters,
    )


def _query_summary(
    connection: sqlite3.Connection,
    start_date: str,
    end_date: str,
    store_id: str | None,
    category: str | None,
    product_id: str | None,
):
    where_clause, parameters = _build_filter_clause(
        start_date,
        end_date,
        store_id,
        category,
        product_id,
    )
    cursor = connection.execute(
        f"""
        SELECT
            ROUND(COALESCE(SUM(s.amount), 0), 2) AS total_sales,
            COUNT(DISTINCT s.order_id) AS order_count,
            COALESCE(SUM(s.qty), 0) AS total_quantity,
            COUNT(DISTINCT s.store_id) AS active_stores
        FROM sales s
        JOIN stores st
            ON s.store_id = st.store_id
        JOIN products p
            ON s.product_id = p.product_id
        WHERE {where_clause}
        """,
        parameters,
    )
    row = cursor.fetchone()
    total_sales = round(float(row[0] or 0), 2)
    order_count = int(row[1] or 0)

    return {
        "total_sales": total_sales,
        "order_count": order_count,
        "avg_order_value": (
            round(total_sales / order_count, 2)
            if order_count
            else None
        ),
        "total_quantity": int(row[2] or 0),
        "active_stores": int(row[3] or 0),
    }


def _query_ranking(
    connection: sqlite3.Connection,
    start_date: str,
    end_date: str,
    store_id: str | None,
    category: str | None,
    product_id: str | None,
    dimension: str,
):
    dimensions = {
        "product": {
            "select": "p.product_id, p.product_name",
            "group": "p.product_id, p.product_name",
            "order": "p.product_name",
        },
        "store": {
            "select": (
                "st.store_id, st.store_name, "
                "st.category, st.district"
            ),
            "group": (
                "st.store_id, st.store_name, "
                "st.category, st.district"
            ),
            "order": "st.store_id",
        },
        "category": {
            "select": "st.category",
            "group": "st.category",
            "order": "st.category",
        },
    }
    config = dimensions[dimension]
    where_clause, parameters = _build_filter_clause(
        start_date,
        end_date,
        store_id,
        category,
        product_id,
    )
    cursor = connection.execute(
        f"""
        SELECT
            {config["select"]},
            ROUND(COALESCE(SUM(s.amount), 0), 2) AS total_sales,
            COUNT(DISTINCT s.order_id) AS order_count,
            COALESCE(SUM(s.qty), 0) AS total_quantity
        FROM sales s
        JOIN stores st
            ON s.store_id = st.store_id
        JOIN products p
            ON s.product_id = p.product_id
        WHERE {where_clause}
        GROUP BY {config["group"]}
        ORDER BY total_sales DESC, {config["order"]} ASC
        """,
        parameters,
    )
    rows = cursor.fetchall()
    total_sales = sum(float(row[-3] or 0) for row in rows)
    ranking = []

    for index, row in enumerate(rows):
        item_sales = round(float(row[-3] or 0), 2)
        item_orders = int(row[-2] or 0)
        item_quantity = int(row[-1] or 0)
        metrics = {
            "rank": index + 1,
            "total_sales": item_sales,
            "order_count": item_orders,
            "avg_order_value": (
                round(item_sales / item_orders, 2)
                if item_orders
                else None
            ),
            "total_quantity": item_quantity,
            "sales_share": (
                round(item_sales / total_sales * 100, 2)
                if total_sales
                else 0.0
            ),
        }

        if dimension == "product":
            item = {
                "product_id": row[0],
                "product_name": row[1],
                **metrics,
            }
        elif dimension == "store":
            item = {
                "store_id": row[0],
                "store_name": row[1],
                "category": row[2],
                "district": row[3],
                **metrics,
            }
        else:
            item = {
                "category": row[0],
                **metrics,
            }

        ranking.append(item)

    return ranking


# 为前端全局筛选提供独立聚合，不改变旧接口契约。
def get_filtered_analytics_data(
    store_id: str | None = None,
    category: str | None = None,
    product_id: str | None = None,
    months: int = 1,
    db_file: str | Path = DB_FILE,
):
    database_path = Path(db_file)

    if not database_path.exists():
        return {
            "success": False,
            "message": "经营数据库不存在",
        }

    try:
        normalized_months = max(
            1,
            min(int(months), 3),
        )
    except (TypeError, ValueError):
        normalized_months = 1

    try:
        with closing(sqlite3.connect(database_path)) as connection:
            latest_result = connection.execute(
                "SELECT MAX(date) FROM sales"
            ).fetchone()
            latest_date_text = (
                latest_result[0]
                if latest_result
                else None
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
            period_start = _add_months(
                latest_month_start,
                -(normalized_months - 1),
            )
            period_end = _add_months(
                latest_month_start,
                1,
            )

            summary = _query_summary(
                connection,
                period_start.isoformat(),
                period_end.isoformat(),
                store_id,
                category,
                product_id,
            )
            product_ranking = _query_ranking(
                connection,
                period_start.isoformat(),
                period_end.isoformat(),
                store_id,
                category,
                product_id,
                "product",
            )
            store_ranking = _query_ranking(
                connection,
                period_start.isoformat(),
                period_end.isoformat(),
                store_id,
                category,
                product_id,
                "store",
            )
            category_ranking = _query_ranking(
                connection,
                period_start.isoformat(),
                period_end.isoformat(),
                store_id,
                category,
                product_id,
                "category",
            )

            trend = []

            for offset in (-2, -1, 0):
                month_start = _add_months(
                    latest_month_start,
                    offset,
                )
                month_end = _add_months(
                    month_start,
                    1,
                )
                month_summary = _query_summary(
                    connection,
                    month_start.isoformat(),
                    month_end.isoformat(),
                    store_id,
                    category,
                    product_id,
                )
                trend.append(
                    {
                        "month": (
                            f"{month_start.year}-"
                            f"{month_start.month:02d}"
                        ),
                        "label": f"{month_start.month}月",
                        **month_summary,
                    }
                )


            if normalized_months == 1 and len(trend) >= 2:
                current_period = trend[-1]
                previous_period = trend[-2]
                summary["sales_change_rate"] = _calculate_change_rate(
                    current_period["total_sales"],
                    previous_period["total_sales"],
                )
                summary["order_change_rate"] = _calculate_change_rate(
                    current_period["order_count"],
                    previous_period["order_count"],
                )
                summary["aov_change_rate"] = _calculate_change_rate(
                    current_period["avg_order_value"],
                    previous_period["avg_order_value"],
                )
            else:
                summary["sales_change_rate"] = None
                summary["order_change_rate"] = None
                summary["aov_change_rate"] = None
            stores = [
                {
                    "store_id": row[0],
                    "store_name": row[1],
                    "category": row[2],
                    "district": row[3],
                }
                for row in connection.execute(
                    """
                    SELECT
                        store_id,
                        store_name,
                        category,
                        district
                    FROM stores
                    ORDER BY store_id
                    """
                ).fetchall()
            ]
            products = [
                {
                    "product_id": row[0],
                    "product_name": row[1],
                }
                for row in connection.execute(
                    """
                    SELECT
                        product_id,
                        product_name
                    FROM products
                    ORDER BY product_name
                    """
                ).fetchall()
            ]

    except (sqlite3.Error, ValueError):
        return {
            "success": False,
            "message": "筛选经营数据查询失败",
        }

    summary["top_product"] = (
        product_ranking[0]
        if product_ranking
        else None
    )
    summary["top_store"] = (
        store_ranking[0]
        if store_ranking
        else None
    )
    summary["top_category"] = (
        category_ranking[0]
        if category_ranking
        else None
    )

    return {
        "success": True,
        "latest_data_date": latest_date_text,
        "period": {
            "months": normalized_months,
            "label": (
                f"{latest_month_start.year}年"
                f"{latest_month_start.month}月"
                if normalized_months == 1
                else "最近3个月"
            ),
            "start_date": period_start.isoformat(),
            "end_date": period_end.isoformat(),
        },
        "applied_filters": {
            "store_id": store_id,
            "category": category,
            "product_id": product_id,
        },
        "filters": {
            "stores": stores,
            "categories": sorted(
                {
                    item["category"]
                    for item in stores
                    if item["category"]
                }
            ),
            "products": products,
        },
        "summary": summary,
        "trend": trend,
        "product_ranking": product_ranking,
        "store_ranking": store_ranking,
        "category_ranking": category_ranking,
        "message": "查询成功",
    }

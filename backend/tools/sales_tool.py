from pathlib import Path
import sqlite3


# 1. 配置数据库路径
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DB_FILE = BASE_DIR / "data" / "moneki.db"


# 2. 查询指定时间段经营汇总
def get_sales_summary(
    start_date: str,
    end_date: str,
):
    conn = sqlite3.connect(DB_FILE)

    cursor = conn.cursor()

    sql = """
    SELECT
        ROUND(SUM(amount), 2) AS total_sales,
        COUNT(DISTINCT order_id) AS order_count,
        ROUND(
            SUM(amount) / COUNT(DISTINCT order_id),
            2
        ) AS avg_order_value
    FROM sales
    WHERE date >= ?
      AND date < ?
    """

    cursor.execute(
        sql,
        (
            start_date,
            end_date,
        ),
    )

    result = cursor.fetchone()

    conn.close()


    # 3. 没有查询到数据
    if result is None or result[0] is None:
        return {
            "success": False,
            "start_date": start_date,
            "end_date": end_date,
            "total_sales": None,
            "order_count": 0,
            "avg_order_value": None,
            "message": "没有查询到经营数据",
        }


    # 4. 返回经营指标
    return {
        "success": True,
        "start_date": start_date,
        "end_date": end_date,
        "total_sales": result[0],
        "order_count": result[1],
        "avg_order_value": result[2],
        "message": "查询成功",
    }


# 5. 对比两个时间段客单价趋势
def compare_avg_order_value(
    current_start: str,
    current_end: str,
    previous_start: str,
    previous_end: str,
):
    current = get_sales_summary(
        current_start,
        current_end,
    )

    previous = get_sales_summary(
        previous_start,
        previous_end,
    )


    # 6. 任意时间段没有数据时返回失败
    if not current["success"] or not previous["success"]:
        return {
            "success": False,
            "message": "无法完成客单价趋势对比",
        }


    # 7. 计算客单价变化
    current_value = current["avg_order_value"]
    previous_value = previous["avg_order_value"]

    change = round(
        current_value - previous_value,
        2,
    )

    change_rate = round(
        change / previous_value * 100,
        2,
    )


    # 8. 判断趋势
    if change > 0:
        trend = "上涨"
    elif change < 0:
        trend = "下降"
    else:
        trend = "持平"


    return {
        "success": True,
        "current_avg_order_value": current_value,
        "previous_avg_order_value": previous_value,
        "change": change,
        "change_rate": change_rate,
        "trend": trend,
        "message": "查询成功",
    }
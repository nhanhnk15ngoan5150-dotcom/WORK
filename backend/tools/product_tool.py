from pathlib import Path
import sqlite3


# 1. 配置数据库路径
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DB_FILE = BASE_DIR / "data" / "moneki.db"


# 2. 查询商品销售额
def get_product_sales(
    product_name: str,
    start_date: str,
    end_date: str,
):
    conn = sqlite3.connect(DB_FILE)

    cursor = conn.cursor()

    sql = """
    SELECT
        p.product_name,
        SUM(s.amount) AS total_sales
    FROM sales s
    JOIN products p
        ON s.product_id = p.product_id
    WHERE p.product_name = ?
      AND s.date >= ?
      AND s.date < ?
    GROUP BY p.product_name
    """

    cursor.execute(
        sql,
        (
            product_name,
            start_date,
            end_date,
        ),
    )

    result = cursor.fetchone()

    conn.close()


    # 3. 没有查询到数据
    if result is None:
        return {
            "success": False,
            "product_name": product_name,
            "start_date": start_date,
            "end_date": end_date,
            "total_sales": None,
            "message": "没有查询到符合条件的商品销售数据",
        }


    # 4. 返回结构化查询结果
    return {
        "success": True,
        "product_name": result[0],
        "start_date": start_date,
        "end_date": end_date,
        "total_sales": round(result[1], 2),
        "message": "查询成功",
    }

# 5. 查询商品销量
def get_product_quantity(
    product_name: str,
    start_date: str,
    end_date: str,
):
    conn = sqlite3.connect(DB_FILE)

    cursor = conn.cursor()

    sql = """
    SELECT
        p.product_name,
        SUM(s.qty) AS total_quantity
    FROM sales s
    JOIN products p
        ON s.product_id = p.product_id
    WHERE p.product_name = ?
      AND s.date >= ?
      AND s.date < ?
    GROUP BY p.product_name
    """

    cursor.execute(
        sql,
        (
            product_name,
            start_date,
            end_date,
        ),
    )

    result = cursor.fetchone()

    conn.close()

    # 6. 没有查询到数据
    if result is None:
        return {
            "success": False,
            "product_name": product_name,
            "start_date": start_date,
            "end_date": end_date,
            "total_quantity": None,
            "message": "没有查询到符合条件的商品销量数据",
        }

    # 7. 返回结构化查询结果
    return {
        "success": True,
        "product_name": result[0],
        "start_date": start_date,
        "end_date": end_date,
        "total_quantity": int(
            result[1]
        ),
        "message": "查询成功",
    }

# 8. 查询商品销售排行榜
def get_product_rank(
    start_date: str,
    end_date: str,
):
    conn = sqlite3.connect(DB_FILE)

    cursor = conn.cursor()

    sql = """
    SELECT
        p.product_name,
        ROUND(SUM(s.amount), 2) AS total_sales,
        SUM(s.qty) AS total_quantity
    FROM sales s
    JOIN products p
        ON s.product_id = p.product_id
    WHERE s.date >= ?
      AND s.date < ?
    GROUP BY p.product_name
    ORDER BY total_sales DESC
    """

    cursor.execute(
        sql,
        (
            start_date,
            end_date,
        ),
    )

    rows = cursor.fetchall()

    conn.close()

    if not rows:
        return {
            "success": False,
            "data": [],
            "message": "没有查询到商品销售数据",
        }


    data = [
        {
            "product_name": row[0],
            "total_sales": row[1],
            "total_quantity": int(row[2]),
        }
        for row in rows
    ]


    return {
        "success": True,
        "start_date": start_date,
        "end_date": end_date,
        "data": data,
        "top_product": data[0],
        "message": "查询成功",
    }
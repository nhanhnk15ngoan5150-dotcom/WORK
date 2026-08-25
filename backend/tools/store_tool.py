from pathlib import Path
import sqlite3


# 1. 配置数据库路径
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DB_FILE = BASE_DIR / "data" / "moneki.db"


# 2. 查询各门店品类营业额
def get_store_category_sales(
    start_date: str,
    end_date: str,
):
    conn = sqlite3.connect(DB_FILE)

    cursor = conn.cursor()

    sql = """
    SELECT
        st.category,
        ROUND(SUM(s.amount), 2) AS total_sales
    FROM sales s
    JOIN stores st
        ON s.store_id = st.store_id
    WHERE s.date >= ?
      AND s.date < ?
    GROUP BY st.category
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


    # 3. 没有查询到数据
    if not rows:
        return {
            "success": False,
            "start_date": start_date,
            "end_date": end_date,
            "data": [],
            "message": "没有查询到门店品类销售数据",
        }


    # 4. 返回结构化结果
    data = [
        {
            "category": row[0],
            "total_sales": row[1],
        }
        for row in rows
    ]

    return {
        "success": True,
        "start_date": start_date,
        "end_date": end_date,
        "data": data,
        "top_category": data[0],
        "message": "查询成功",
    }
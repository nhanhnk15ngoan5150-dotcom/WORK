from pathlib import Path
import sqlite3

import pandas as pd


# 1. 配置项目路径
BASE_DIR = Path(__file__).resolve().parent.parent

PROCESSED_DIR = BASE_DIR / "data" / "processed"

SALES_FILE = PROCESSED_DIR / "sales.csv"
STORES_FILE = PROCESSED_DIR / "stores.csv"
PRODUCTS_FILE = PROCESSED_DIR / "products.csv"

DB_FILE = BASE_DIR / "data" / "moneki.db"


# 2. 读取清洗后的数据
sales = pd.read_csv(SALES_FILE)
stores = pd.read_csv(STORES_FILE)
products = pd.read_csv(PRODUCTS_FILE)

print("sales 数据量：", len(sales))
print("stores 数据量：", len(stores))
print("products 数据量：", len(products))


# 3. 创建 SQLite 数据库连接
conn = sqlite3.connect(DB_FILE)


# 4. 写入数据库
sales.to_sql(
    "sales",
    conn,
    if_exists="replace",
    index=False,
)

stores.to_sql(
    "stores",
    conn,
    if_exists="replace",
    index=False,
)

products.to_sql(
    "products",
    conn,
    if_exists="replace",
    index=False,
)


# 5. 创建常用查询索引
cursor = conn.cursor()

cursor.execute(
    "CREATE INDEX IF NOT EXISTS idx_sales_date "
    "ON sales(date)"
)

cursor.execute(
    "CREATE INDEX IF NOT EXISTS idx_sales_store "
    "ON sales(store_id)"
)

cursor.execute(
    "CREATE INDEX IF NOT EXISTS idx_sales_product "
    "ON sales(product_id)"
)

conn.commit()


# 6. 验证数据库数据量
sales_count = cursor.execute(
    "SELECT COUNT(*) FROM sales"
).fetchone()[0]

stores_count = cursor.execute(
    "SELECT COUNT(*) FROM stores"
).fetchone()[0]

products_count = cursor.execute(
    "SELECT COUNT(*) FROM products"
).fetchone()[0]

print("\n===== SQLite 数据验证 =====")
print("sales：", sales_count)
print("stores：", stores_count)
print("products：", products_count)


# 7. 关闭数据库连接
conn.close()

print("\n数据库创建成功：", DB_FILE)
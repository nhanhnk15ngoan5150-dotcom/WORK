from pathlib import Path

import pandas as pd


# 1. 配置项目路径
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

SALES_FILE = DATA_DIR / "sales.csv"
STORES_FILE = DATA_DIR / "stores.csv"
PRODUCTS_FILE = DATA_DIR / "products.csv"

PROCESSED_DIR = DATA_DIR / "processed"


# 2. 读取原始数据
sales = pd.read_csv(SALES_FILE)
stores = pd.read_csv(STORES_FILE)
products = pd.read_csv(PRODUCTS_FILE)

print("原始 sales 数据量：", len(sales))
print("原始 stores 数据量：", len(stores))
print("原始 products 数据量：", len(products))


# 3. 删除完全重复行
before_duplicates = len(sales)

sales = sales.drop_duplicates()

print("删除重复 sales 数据：", before_duplicates - len(sales), "条")


# 4. 标准化字段格式
sales["store_id"] = (
    sales["store_id"]
    .astype(str)
    .str.strip()
    .str.upper()
)

sales["product_id"] = (
    sales["product_id"]
    .astype(str)
    .str.strip()
    .str.upper()
)

products["product_id"] = (
    products["product_id"]
    .astype(str)
    .str.strip()
    .str.upper()
)

stores["store_id"] = (
    stores["store_id"]
    .astype(str)
    .str.strip()
    .str.upper()
)

# 5. 标准化日期格式
sales["date"] = pd.to_datetime(
    sales["date"],
    dayfirst=True,
    errors="coerce",
).dt.strftime("%Y-%m-%d")

# 6. 标准化数值字段类型
sales["qty"] = pd.to_numeric(
    sales["qty"],
    errors="coerce",
)

sales["amount"] = pd.to_numeric(
    sales["amount"],
    errors="coerce",
)

products["unit_price"] = pd.to_numeric(
    products["unit_price"],
    errors="coerce",
)


# 7. 删除无效外键数据
invalid_product = ~sales["product_id"].isin(products["product_id"])
invalid_store = ~sales["store_id"].isin(stores["store_id"])

print("删除无效 product_id 数据：", invalid_product.sum(), "条")
print("删除无效 store_id 数据：", invalid_store.sum(), "条")

sales = sales[
    ~invalid_product
    & ~invalid_store
].copy()


# 8. 合并商品价格
sales = sales.merge(
    products[["product_id", "unit_price"]],
    on="product_id",
    how="left",
)


# 9. 删除明显异常交易
invalid_transaction = (
    sales["qty"].isna()
    | (sales["qty"] <= 0)
    | (
        sales["amount"].notna()
        & (sales["amount"] < 0)
    )
)

print("删除异常交易数据：", invalid_transaction.sum(), "条")

sales = sales[
    ~invalid_transaction
].copy()


# 10. 补全缺失 amount
missing_amount_before = sales["amount"].isna().sum()

mask = sales["amount"].isna()

sales.loc[mask, "amount"] = (
    sales.loc[mask, "qty"]
    * sales.loc[mask, "unit_price"]
)

missing_amount_after = sales["amount"].isna().sum()

print(
    "amount 补全数量：",
    missing_amount_before - missing_amount_after,
)

print(
    "amount 剩余缺失：",
    missing_amount_after,
)


# 11. 验证 amount 计算规则
sales["expected_amount"] = (
    sales["qty"]
    * sales["unit_price"]
)

valid_amount = (
    sales["amount"].notna()
    & sales["expected_amount"].notna()
)

amount_match = (
    sales.loc[valid_amount, "amount"].round(2)
    == sales.loc[valid_amount, "expected_amount"].round(2)
)

print("amount 规则验证数据量：", len(amount_match))
print("amount 规则匹配数量：", amount_match.sum())
print("amount 规则不匹配数量：", (~amount_match).sum())
print("amount 规则匹配率：", f"{amount_match.mean():.2%}")


# 12. 删除临时字段
sales = sales.drop(
    columns=[
        "unit_price",
        "expected_amount",
    ]
)


# 13. 创建清洗数据目录
PROCESSED_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


# 14. 保存清洗后的数据
sales.to_csv(
    PROCESSED_DIR / "sales.csv",
    index=False,
)

stores.to_csv(
    PROCESSED_DIR / "stores.csv",
    index=False,
)

products.to_csv(
    PROCESSED_DIR / "products.csv",
    index=False,
)


# 15. 最终检查
print("\n===== 清洗完成 =====")

print("最终 sales 数据量：", len(sales))
print("最终 amount 缺失：", sales["amount"].isna().sum())
print("最终重复数据：", sales.duplicated().sum())

print(
    "最终无效 product_id：",
    (~sales["product_id"].isin(products["product_id"])).sum(),
)

print(
    "最终无效 store_id：",
    (~sales["store_id"].isin(stores["store_id"])).sum(),
)

print(
    "清洗数据保存位置：",
    PROCESSED_DIR,
)
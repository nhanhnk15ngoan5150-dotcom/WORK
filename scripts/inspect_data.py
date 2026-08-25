from pathlib import Path

import pandas as pd


# ==============================
# 项目路径
# ==============================

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

# 根据你实际的数据目录修改
RAW_DATA_DIR = DATA_DIR

SALES_FILE = RAW_DATA_DIR / "sales.csv"
STORES_FILE = RAW_DATA_DIR / "stores.csv"
PRODUCTS_FILE = RAW_DATA_DIR / "products.csv"


# ==============================
# 读取数据
# ==============================

sales_df = pd.read_csv(SALES_FILE)
stores_df = pd.read_csv(STORES_FILE)
products_df = pd.read_csv(PRODUCTS_FILE)


# ==============================
# 查看数据
# ==============================

print("\n===== SALES =====")
print(sales_df.head())

print("\n===== STORES =====")
print(stores_df.head())

print("\n===== PRODUCTS =====")
print(products_df.head())


# ==============================
# 查看字段
# ==============================

print("\n===== SALES COLUMNS =====")
print(sales_df.columns.tolist())

print("\n===== STORES COLUMNS =====")
print(stores_df.columns.tolist())

print("\n===== PRODUCTS COLUMNS =====")
print(products_df.columns.tolist())


# ==============================
# 缺失值
# ==============================

print("\n===== SALES 缺失值 =====")
print(sales_df.isnull().sum())

print("\n===== STORES 缺失值 =====")
print(stores_df.isnull().sum())

print("\n===== PRODUCTS 缺失值 =====")
print(products_df.isnull().sum())


# ==============================
# 重复数据
# ==============================

print("\n===== 重复行 =====")
print("sales:", sales_df.duplicated().sum())
print("stores:", stores_df.duplicated().sum())
print("products:", products_df.duplicated().sum())
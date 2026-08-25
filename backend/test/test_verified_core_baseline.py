import sqlite3
import unittest
from pathlib import Path

# 1. 定位项目真实数据库
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DB_FILE = PROJECT_ROOT / "data" / "moneki.db"

from services.time_service import parse_time_expression
from tools.dashboard_tool import get_dashboard_data
from tools.product_tool import (
    get_product_quantity,
    get_product_rank,
    get_product_sales,
)
from tools.sales_tool import get_sales_summary
from tools.store_tool import get_store_category_sales


class VerifiedCoreBaselineTest(unittest.TestCase):

    # 1. 锁定当前数据集基线
    def test_database_baseline(self):
        connection = sqlite3.connect(DB_FILE)

        try:
            row = connection.execute(
                """
                SELECT MIN(date), MAX(date), COUNT(*)
                FROM sales
                """
            ).fetchone()

            store_count = connection.execute(
                "SELECT COUNT(*) FROM stores"
            ).fetchone()[0]

            product_count = connection.execute(
                "SELECT COUNT(*) FROM products"
            ).fetchone()[0]
        finally:
            connection.close()

        self.assertEqual(
            row,
            ("2026-05-01", "2026-07-31", 11944),
        )
        self.assertEqual(store_count, 5)
        self.assertEqual(product_count, 20)

    # 2. 锁定时间解析基线
    def test_time_service_baseline(self):
        self.assertEqual(
            parse_time_expression("五月"),
            {
                "start_date": "2026-05-01",
                "end_date": "2026-06-01",
                "mode": "month",
            },
        )

        self.assertEqual(
            parse_time_expression("七月"),
            {
                "start_date": "2026-07-01",
                "end_date": "2026-08-01",
                "mode": "month",
            },
        )

        self.assertEqual(
            parse_time_expression("最近"),
            {
                "current_start": "2026-07-01",
                "current_end": "2026-08-01",
                "previous_start": "2026-06-01",
                "previous_end": "2026-07-01",
                "mode": "compare",
            },
        )

        self.assertEqual(
            parse_time_expression("四月")["mode"],
            "out_of_range",
        )
        self.assertEqual(
            parse_time_expression("八月")["mode"],
            "out_of_range",
        )

    # 3. 锁定经营汇总基线
    def test_sales_summary_baseline(self):
        expected = {
            "2026-05-01": (139754.0, 3806, 36.72),
            "2026-06-01": (132820.0, 3776, 35.17),
            "2026-07-01": (151572.0, 4212, 35.99),
        }

        periods = {
            "2026-05-01": "2026-06-01",
            "2026-06-01": "2026-07-01",
            "2026-07-01": "2026-08-01",
        }

        for start_date, values in expected.items():
            result = get_sales_summary(
                start_date,
                periods[start_date],
            )

            self.assertTrue(result["success"])
            self.assertEqual(result["total_sales"], values[0])
            self.assertEqual(result["order_count"], values[1])
            self.assertEqual(result["avg_order_value"], values[2])

    # 4. 锁定商品查询基线
    def test_product_baseline(self):
        quantity = get_product_quantity(
            "可乐",
            "2026-06-01",
            "2026-07-01",
        )
        sales = get_product_sales(
            "可乐",
            "2026-06-01",
            "2026-07-01",
        )
        ranking = get_product_rank(
            "2026-07-01",
            "2026-08-01",
        )

        self.assertTrue(quantity["success"])
        self.assertEqual(quantity["total_quantity"], 310)

        self.assertTrue(sales["success"])
        self.assertEqual(sales["total_sales"], 1550.0)

        self.assertTrue(ranking["success"])
        self.assertEqual(len(ranking["data"]), 20)
        self.assertEqual(
            ranking["data"][:3],
            [
                {
                    "product_name": "三文鱼poke",
                    "total_sales": 14478.0,
                    "total_quantity": 381,
                },
                {
                    "product_name": "牛肉poke",
                    "total_sales": 13314.0,
                    "total_quantity": 317,
                },
                {
                    "product_name": "鸡肉poke",
                    "total_sales": 12852.0,
                    "total_quantity": 378,
                },
            ],
        )

    # 5. 锁定 Dashboard 基线
    def test_dashboard_baseline(self):
        result = get_dashboard_data()

        self.assertTrue(result["success"])
        self.assertEqual(result["latest_data_date"], "2026-07-31")
        self.assertEqual(result["period"]["label"], "2026年7月")
        self.assertEqual(result["summary"]["total_sales"], 151572.0)
        self.assertEqual(result["summary"]["order_count"], 4212)
        self.assertEqual(result["summary"]["avg_order_value"], 35.99)
        self.assertEqual(result["summary"]["top_category"], "日料")
        self.assertEqual(
            [item["total_sales"] for item in result["trend"]],
            [139754.0, 132820.0, 151572.0],
        )

    # 6. 锁定门店品类基线
    def test_store_category_baseline(self):
        result = get_store_category_sales(
            "2026-07-01",
            "2026-08-01",
        )

        self.assertTrue(result["success"])
        self.assertEqual(
            result["top_category"],
            {
                "category": "日料",
                "total_sales": 32301.0,
            },
        )
        self.assertEqual(len(result["data"]), 5)


if __name__ == "__main__":
    unittest.main()

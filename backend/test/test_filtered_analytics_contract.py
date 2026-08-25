from contextlib import closing
import sqlite3
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from tools.analytics_tool import get_filtered_analytics_data


class FilteredAnalyticsContractTest(unittest.TestCase):
    def _create_database(self, database_path: Path):
        with closing(sqlite3.connect(database_path)) as connection:
            connection.executescript(
                """
                CREATE TABLE stores (
                    store_id TEXT,
                    store_name TEXT,
                    category TEXT,
                    district TEXT
                );
                CREATE TABLE products (
                    product_id TEXT,
                    product_name TEXT
                );
                CREATE TABLE sales (
                    order_id TEXT,
                    date TEXT,
                    store_id TEXT,
                    product_id TEXT,
                    qty INTEGER,
                    amount REAL,
                    payment TEXT
                );
                """
            )
            connection.executemany(
                "INSERT INTO stores VALUES (?, ?, ?, ?)",
                [
                    ("S01", "一号店", "拉面", "徐汇"),
                    ("S02", "二号店", "轻食", "静安"),
                ],
            )
            connection.executemany(
                "INSERT INTO products VALUES (?, ?)",
                [
                    ("P01", "面"),
                    ("P02", "饭"),
                ],
            )
            connection.executemany(
                "INSERT INTO sales VALUES (?, ?, ?, ?, ?, ?, ?)",
                [
                    ("M01", "2026-05-05", "S01", "P01", 1, 50, "card"),
                    ("J01", "2026-06-05", "S02", "P02", 2, 80, "card"),
                    ("A01", "2026-07-05", "S01", "P01", 2, 100, "cash"),
                    ("A02", "2026-07-06", "S02", "P02", 3, 150, "card"),
                ],
            )

            connection.commit()

    def test_default_latest_month_keeps_full_dimensions(self):
        with TemporaryDirectory() as temporary_directory:
            database_path = Path(temporary_directory) / "analytics.db"
            self._create_database(database_path)

            result = get_filtered_analytics_data(
                db_file=database_path
            )

        self.assertTrue(result["success"])
        self.assertEqual(result["period"]["months"], 1)
        self.assertEqual(result["summary"]["total_sales"], 250.0)
        self.assertEqual(result["summary"]["order_count"], 2)
        self.assertEqual(result["summary"]["avg_order_value"], 125.0)
        self.assertEqual(result["summary"]["sales_change_rate"], 212.5)
        self.assertEqual(result["summary"]["order_change_rate"], 100.0)
        self.assertEqual(result["summary"]["aov_change_rate"], 56.25)
        self.assertEqual(result["summary"]["total_quantity"], 5)
        self.assertEqual(len(result["filters"]["stores"]), 2)
        self.assertEqual(len(result["filters"]["products"]), 2)
        self.assertEqual(len(result["product_ranking"]), 2)
        self.assertEqual(len(result["store_ranking"]), 2)

    def test_filters_and_three_month_scope_are_applied_together(self):
        with TemporaryDirectory() as temporary_directory:
            database_path = Path(temporary_directory) / "analytics.db"
            self._create_database(database_path)

            result = get_filtered_analytics_data(
                store_id="S01",
                category="拉面",
                product_id="P01",
                months=3,
                db_file=database_path,
            )

        self.assertTrue(result["success"])
        self.assertEqual(result["period"]["months"], 3)
        self.assertEqual(result["summary"]["total_sales"], 150.0)
        self.assertIsNone(result["summary"]["sales_change_rate"])
        self.assertEqual(result["summary"]["order_count"], 2)
        self.assertEqual(result["summary"]["total_quantity"], 3)
        self.assertEqual(
            [item["total_sales"] for item in result["trend"]],
            [50.0, 0.0, 100.0],
        )
        self.assertEqual(
            result["product_ranking"][0]["product_name"],
            "面",
        )
        self.assertEqual(
            result["store_ranking"][0]["store_name"],
            "一号店",
        )


if __name__ == "__main__":
    unittest.main()

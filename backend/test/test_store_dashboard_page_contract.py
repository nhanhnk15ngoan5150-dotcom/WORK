from contextlib import closing
import sqlite3
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from tools.store_dashboard_tool import get_store_dashboard_data


class StoreDashboardContractTest(unittest.TestCase):
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
                """
                INSERT INTO stores (
                    store_id,
                    store_name,
                    category,
                    district
                ) VALUES (?, ?, ?, ?)
                """,
                [
                    ("S01", "一号店", "拉面", "徐汇"),
                    ("S02", "二号店", "轻食", "静安"),
                ],
            )
            connection.executemany(
                """
                INSERT INTO sales (
                    order_id,
                    date,
                    store_id,
                    product_id,
                    qty,
                    amount,
                    payment
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                [
                    ("M01", "2026-05-08", "S01", "P01", 2, 100, "card"),
                    ("J01", "2026-06-08", "S02", "P01", 3, 200, "card"),
                    ("A01", "2026-07-02", "S01", "P01", 1, 100, "card"),
                    ("A01", "2026-07-02", "S01", "P02", 2, 50, "card"),
                    ("A02", "2026-07-03", "S02", "P01", 4, 200, "cash"),
                ],
            )

            connection.commit()

    def test_returns_latest_month_summary_filters_ranking_and_trend(self):
        with TemporaryDirectory() as temporary_directory:
            database_path = Path(temporary_directory) / "stores.db"
            self._create_database(database_path)

            result = get_store_dashboard_data(database_path)

        self.assertTrue(result["success"])
        self.assertEqual(result["latest_data_date"], "2026-07-03")
        self.assertEqual(result["period"]["label"], "2026年7月")
        self.assertEqual(result["summary"]["total_stores"], 2)
        self.assertEqual(result["summary"]["active_stores"], 2)
        self.assertEqual(result["summary"]["total_sales"], 350.0)
        self.assertEqual(result["summary"]["order_count"], 2)
        self.assertEqual(result["summary"]["avg_order_value"], 175.0)
        self.assertEqual(result["summary"]["total_quantity"], 7)
        self.assertEqual(
            result["summary"]["top_store"]["store_id"],
            "S02",
        )
        self.assertEqual(
            result["filters"]["categories"],
            ["拉面", "轻食"],
        )
        self.assertEqual(
            result["filters"]["districts"],
            ["徐汇", "静安"],
        )
        self.assertEqual(
            [item["store_id"] for item in result["ranking"]],
            ["S02", "S01"],
        )
        self.assertEqual(
            [item["total_sales"] for item in result["trend"]],
            [100.0, 200.0, 350.0],
        )
        self.assertTrue(
            all(len(item["stores"]) == 2 for item in result["trend"])
        )

    def test_missing_database_does_not_create_a_file(self):
        with TemporaryDirectory() as temporary_directory:
            database_path = Path(temporary_directory) / "missing.db"

            result = get_store_dashboard_data(database_path)

            self.assertFalse(result["success"])
            self.assertFalse(database_path.exists())


if __name__ == "__main__":
    unittest.main()
from contextlib import closing
import sqlite3
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from tools.store_dashboard_tool import get_store_dashboard_data


class StoreDashboardContractTest(unittest.TestCase):
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
                """
                INSERT INTO stores (
                    store_id,
                    store_name,
                    category,
                    district
                ) VALUES (?, ?, ?, ?)
                """,
                [
                    ("S01", "一号店", "拉面", "徐汇"),
                    ("S02", "二号店", "轻食", "静安"),
                ],
            )
            connection.executemany(
                """
                INSERT INTO sales (
                    order_id,
                    date,
                    store_id,
                    product_id,
                    qty,
                    amount,
                    payment
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                [
                    ("M01", "2026-05-08", "S01", "P01", 2, 100, "card"),
                    ("J01", "2026-06-08", "S02", "P01", 3, 200, "card"),
                    ("A01", "2026-07-02", "S01", "P01", 1, 100, "card"),
                    ("A01", "2026-07-02", "S01", "P02", 2, 50, "card"),
                    ("A02", "2026-07-03", "S02", "P01", 4, 200, "cash"),
                ],
            )

            connection.commit()

    def test_returns_latest_month_summary_filters_ranking_and_trend(self):
        with TemporaryDirectory() as temporary_directory:
            database_path = Path(temporary_directory) / "stores.db"
            self._create_database(database_path)

            result = get_store_dashboard_data(database_path)

        self.assertTrue(result["success"])
        self.assertEqual(result["latest_data_date"], "2026-07-03")
        self.assertEqual(result["period"]["label"], "2026年7月")
        self.assertEqual(result["summary"]["total_stores"], 2)
        self.assertEqual(result["summary"]["active_stores"], 2)
        self.assertEqual(result["summary"]["total_sales"], 350.0)
        self.assertEqual(result["summary"]["order_count"], 2)
        self.assertEqual(result["summary"]["avg_order_value"], 175.0)
        self.assertEqual(result["summary"]["total_quantity"], 7)
        self.assertEqual(
            result["summary"]["top_store"]["store_id"],
            "S02",
        )
        self.assertEqual(
            result["filters"]["categories"],
            ["拉面", "轻食"],
        )
        self.assertEqual(
            result["filters"]["districts"],
            ["徐汇", "静安"],
        )
        self.assertEqual(
            [item["store_id"] for item in result["ranking"]],
            ["S02", "S01"],
        )
        self.assertEqual(
            [item["total_sales"] for item in result["trend"]],
            [100.0, 200.0, 350.0],
        )
        self.assertTrue(
            all(len(item["stores"]) == 2 for item in result["trend"])
        )

    def test_cross_store_order_is_counted_once_in_period_total(self):
        with TemporaryDirectory() as temporary_directory:
            database_path = Path(temporary_directory) / "stores.db"
            self._create_database(database_path)

            with closing(sqlite3.connect(database_path)) as connection:
                connection.execute(
                    """
                    INSERT INTO sales (
                        order_id,
                        date,
                        store_id,
                        product_id,
                        qty,
                        amount,
                        payment
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        "M01",
                        "2026-05-08",
                        "S02",
                        "P02",
                        1,
                        50,
                        "card",
                    ),
                )
                connection.commit()

            result = get_store_dashboard_data(database_path)

        may_trend = result["trend"][0]

        self.assertEqual(may_trend["total_sales"], 150.0)
        self.assertEqual(may_trend["order_count"], 1)
        self.assertEqual(
            sum(
                item["order_count"]
                for item in may_trend["stores"]
            ),
            2,
        )

    def test_missing_database_does_not_create_a_file(self):
        with TemporaryDirectory() as temporary_directory:
            database_path = Path(temporary_directory) / "missing.db"

            result = get_store_dashboard_data(database_path)

            self.assertFalse(result["success"])
            self.assertFalse(database_path.exists())


if __name__ == "__main__":
    unittest.main()


import unittest
from unittest.mock import patch
from io import StringIO

from finance_tracker.expense import Expense
from finance_tracker.reports import (
    category_breakdown,
    expense_statistics,
    monthly_report,
)


class TestReports(unittest.TestCase):

    def setUp(self):
        self.expenses = [
            Expense("2026-10-05", 100, "Food", "Lunch"),
            Expense("2026-10-10", 200, "Travel", "Bus"),
            Expense("2026-09-15", 50, "Food", "Snack"),
        ]

    def test_category_breakdown(self):
        result = category_breakdown(self.expenses)

        self.assertEqual(result["Food"], 150)
        self.assertEqual(result["Travel"], 200)

    def test_expense_statistics(self):
        result = expense_statistics(self.expenses)

        self.assertEqual(result["count"], 3)
        self.assertEqual(result["total"], 350)
        self.assertAlmostEqual(result["average"], 350 / 3)
        self.assertEqual(result["highest"], 200)
        self.assertEqual(result["lowest"], 50)

    def test_empty_statistics(self):
        result = expense_statistics([])
        self.assertEqual(result, {})

    def test_monthly_report(self):
        with patch("sys.stdout", new_callable=StringIO) as output:
            result = monthly_report(self.expenses, 2026, 10)

        self.assertEqual(result, 300)
        self.assertIn("Total spent: Rs. 300.00", output.getvalue())

    def test_empty_monthly_report(self):
        with patch("sys.stdout", new_callable=StringIO):
            result = monthly_report([], 2026, 10)

        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()

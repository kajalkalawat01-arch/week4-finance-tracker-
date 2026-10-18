
import unittest
from finance_tracker.expense import Expense


class TestExpense(unittest.TestCase):

    def test_valid_expense(self):
        expense = Expense(
            "2026-10-18", 150, "Food", "Lunch"
        )
        self.assertEqual(expense.amount, 150)
        self.assertEqual(expense.category, "Food")

    def test_invalid_date(self):
        with self.assertRaises(ValueError):
            Expense.validate(
                "18-10-2026", 150, "Food", "Lunch"
            )

    def test_invalid_amount(self):
        with self.assertRaises(ValueError):
            Expense.validate(
                "2026-10-18", -50, "Food", "Lunch"
            )

    def test_empty_description(self):
        with self.assertRaises(ValueError):
            Expense.validate(
                "2026-10-18", 100, "Food", " "
            )

    def test_convert_to_dictionary(self):
        expense = Expense(
            "2026-10-18", 200, "Shopping", "Shoes"
        )
        data = expense.to_dict()
        self.assertEqual(data["amount"], 200)
        self.assertEqual(data["description"], "Shoes")


if __name__ == "__main__":
    unittest.main()

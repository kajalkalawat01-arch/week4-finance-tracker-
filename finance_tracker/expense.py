
from datetime import datetime


class Expense:
    CATEGORIES = [
        "Food",
        "Travel",
        "Shopping",
        "Education",
        "Bills",
        "Health",
        "Other"
    ]

    def __init__(self, date, amount, category, description):
        self.date = date
        self.amount = float(amount)
        self.category = category
        self.description = description

    @staticmethod
    def validate(date, amount, category, description):
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Date must be YYYY-MM-DD.")

        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError("Amount must be greater than zero.")
        except (TypeError, ValueError):
            raise ValueError("Enter a valid positive amount.")

        if category not in Expense.CATEGORIES:
            raise ValueError("Select a valid expense category.")

        if not description.strip():
            raise ValueError("Description cannot be empty.")

        return True

    def to_dict(self):
        return {
            "date": self.date,
            "amount": self.amount,
            "category": self.category,
            "description": self.description
        }

    @classmethod
    def from_dict(cls, data):
        expense = cls(
            data["date"],
            data["amount"],
            data["category"],
            data["description"]
        )
        cls.validate(
            expense.date,
            expense.amount,
            expense.category,
            expense.description
        )
        return expense

    def __str__(self):
        return (
            f"{self.date} | Rs. {self.amount:.2f} | "
            f"{self.category} | {self.description}"
      )
      

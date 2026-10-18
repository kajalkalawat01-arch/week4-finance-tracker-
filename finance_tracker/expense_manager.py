
from datetime import datetime
from .expense import Expense


class ExpenseManager:
    def __init__(self):
        self.expenses = []

    def add_expense(self, expense):
        if not isinstance(expense, Expense):
            raise TypeError("Expected an Expense object.")
        Expense.validate(
            expense.date,
            expense.amount,
            expense.category,
            expense.description
        )
        self.expenses.append(expense)

    def remove_expense(self, index):
        if index < 0 or index >= len(self.expenses):
            raise IndexError("Expense not found.")
        return self.expenses.pop(index)

    def search_expenses(self, keyword):
        keyword = keyword.strip().lower()
        return [
            expense for expense in self.expenses
            if keyword in expense.description.lower()
            or keyword in expense.category.lower()
            or keyword in expense.date.lower()
        ]

    def filter_by_category(self, category):
        return [
            expense for expense in self.expenses
            if expense.category.lower() == category.lower()
        ]

    def filter_by_month(self, year, month):
        return [
            expense for expense in self.expenses
            if datetime.strptime(
                expense.date, "%Y-%m-%d"
            ).year == year
            and datetime.strptime(
                expense.date, "%Y-%m-%d"
            ).month == month
        ]

    def total_expenses(self):
        return sum(expense.amount for expense in self.expenses)
      

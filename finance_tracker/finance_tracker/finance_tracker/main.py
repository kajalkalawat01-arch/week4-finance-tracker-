
from datetime import datetime
from .expense import Expense
from .expense_manager import ExpenseManager
from .file_handler import (
    save_expenses,
    load_expenses,
    export_to_csv,
    backup_data,
    restore_backup,
)
from .reports import (
    monthly_report,
    category_breakdown,
    expense_statistics,
    expense_chart,
)
from .utils import get_valid_date, get_valid_amount, pause, print_heading


class FinanceTracker:
    def __init__(self):
        self.manager = ExpenseManager()
        try:
            self.manager.expenses = load_expenses()
        except (RuntimeError, ValueError) as error:
            print(f"Could not load saved data: {error}")
            print("Starting with an empty expense list.")

    def save(self):
        try:
            save_expenses(self.manager.expenses)
        except RuntimeError as error:
            print(error)

    def add_expense(self):
        print_heading("ADD NEW EXPENSE")
        date = get_valid_date()
        amount = get_valid_amount()

        print("Categories:", ", ".join(Expense.CATEGORIES))
        category = input("Enter category: ").strip().title()
        description = input("Enter description: ").strip()

        try:
            expense = Expense(date, amount, category, description)
            Expense.validate(date, amount, category, description)
            self.manager.add_expense(expense)
            self.save()
            print("Expense added successfully!")
        except (ValueError, TypeError) as error:
            print(f"Could not add expense: {error}")

    def view_expenses(self):
        print_heading("ALL EXPENSES")
        if not self.manager.expenses:
            print("No expenses recorded yet.")
            return

        for number, expense in enumerate(self.manager.expenses, start=1):
            print(f"{number}. {expense}")

        print(f"\nTotal: Rs. {self.manager.total_expenses():.2f}")

    def search_expenses(self):
        keyword = input("Search description, category or date: ").strip()
        results = self.manager.search_expenses(keyword)

        if not results:
            print("No matching expenses found.")
            return

        for expense in results:
            print(expense)

    def generate_monthly_report(self):
        try:
            year = int(input("Enter year (e.g. 2026): "))
            month = int(input("Enter month (1-12): "))
            if not 1 <= month <= 12 or year < 1:
                raise ValueError
            monthly_report(self.manager.expenses, year, month)
        except ValueError:
            print("Enter a valid year and month.")

    def view_category_breakdown(self):
        category_breakdown(self.manager.expenses)
        expense_chart(self.manager.expenses)

    def set_budget(self):
        try:
            budget = get_valid_amount("Enter monthly budget (Rs.): ")
            year = int(input("Budget year: "))
            month = int(input("Budget month (1-12): "))

            if year < 1 or not 1 <= month <= 12:
                raise ValueError

            spent = sum(
                e.amount for e in self.manager.expenses
                if datetime.strptime(e.date, "%Y-%m-%d").year == year
                and datetime.strptime(e.date, "%Y-%m-%d").month == month
            )

            print(f"Budget: Rs. {budget:.2f}")
            print(f"Spent: Rs. {spent:.2f}")
            print(f"Remaining: Rs. {budget - spent:.2f}")
            if spent > budget:
                print("Warning: You are over budget!")
        except ValueError:
            print("Invalid year or month.")

    def export_data(self):
        try:
            path = export_to_csv(self.manager.expenses)
            print(f"CSV exported to: {path}")
        except RuntimeError as error:
            print(error)

    def view_statistics(self):
        expense_statistics(self.manager.expenses)

    def backup_restore(self):
        print("1. Create backup")
        print("2. Restore backup")
        choice = input("Choose 1 or 2: ").strip()

        try:
            if choice == "1":
                print(f"Backup saved: {backup_data()}")
            elif choice == "2":
                confirm = input("Restore backup? Current data may be replaced (yes/no): ")
                if confirm.strip().lower() == "yes":
                    self.manager.expenses = load_expenses() if False else self.manager.expenses
                    restore_backup()
                    self.manager.expenses = load_expenses()
                    print("Backup restored successfully.")
            else:
                print("Invalid choice.")
        except (RuntimeError, OSError, ValueError) as error:
            print(f"Backup operation failed: {error}")

    def run(self):
        while True:
            print_heading("PERSONAL FINANCE TRACKER")
            print("1. Add New Expense")
            print("2. View All Expenses")
            print("3. Search Expenses")
            print("4. Generate Monthly Report")
            print("5. View Category Breakdown")
            print("6. Check Monthly Budget")
            print("7. Export Data to CSV")
            print("8. View Statistics")
            print("9. Backup / Restore Data")
            print("0. Exit")

            choice = input("\nEnter your choice (0-9): ").strip()

            if choice == "1":
                self.add_expense()
            elif choice == "2":
                self.view_expenses()
            elif choice == "3":
                self.search_expenses()
            elif choice == "4":
                self.generate_monthly_report()
            elif choice == "5":
                self.view_category_breakdown()
            elif choice == "6":
                self.set_budget()
            elif choice == "7":
                self.export_data()
            elif choice == "8":
                self.view_statistics()
            elif choice == "9":
                self.backup_restore()
            elif choice == "0":
                print("Thank you for using Personal Finance Tracker!")
                break
            else:
                print("Invalid choice. Please enter 0-9.")


def main():
    tracker = FinanceTracker()
    tracker.run()


if __name__ == "__main__":
    main()

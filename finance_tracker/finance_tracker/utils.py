
from datetime import datetime


def get_valid_date(prompt="Enter date (YYYY-MM-DD): "):
    while True:
        value = input(prompt).strip()
        try:
            datetime.strptime(value, "%Y-%m-%d")
            return value
        except ValueError:
            print("Invalid date. Example: 2026-10-18")


def get_valid_amount(prompt="Enter amount (Rs.): "):
    while True:
        try:
            amount = float(input(prompt).strip())
            if amount > 0:
                return amount
            print("Amount must be greater than zero.")
        except ValueError:
            print("Please enter a valid number.")


def get_valid_choice(prompt, valid_choices):
    valid_choices = [str(choice) for choice in valid_choices]

    while True:
        choice = input(prompt).strip()
        if choice in valid_choices:
            return choice
        print("Invalid choice. Please try again.")


def pause():
    input("\nPress Enter to continue...")


def print_heading(title):
    print("\n" + "=" * 45)
    print(title.center(45))
    print("=" * 45)
  

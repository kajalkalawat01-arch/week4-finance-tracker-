
from collections import defaultdict


def monthly_report(expenses, year, month):
    filtered = [
        e for e in expenses
        if int(e.date[:4]) == year and int(e.date[5:7]) == month
    ]

    total = sum(e.amount for e in filtered)

    print(f"\nMONTHLY REPORT: {year}-{month:02d}")
    print("-" * 40)
    print(f"Number of expenses: {len(filtered)}")
    print(f"Total spent: Rs. {total:.2f}")

    if not filtered:
        print("No expenses found for this month.")
        return

    print("\nExpense details:")
    for expense in filtered:
        print(expense)

    return total


def category_breakdown(expenses):
    totals = defaultdict(float)

    for expense in expenses:
        totals[expense.category] += expense.amount

    print("\nCATEGORY BREAKDOWN")
    print("-" * 40)

    if not totals:
        print("No expenses recorded yet.")
        return {}

    for category, amount in sorted(totals.items()):
        print(f"{category}: Rs. {amount:.2f}")

    return dict(totals)


def expense_statistics(expenses):
    if not expenses:
        print("No data available for statistics.")
        return {}

    amounts = [e.amount for e in expenses]
    total = sum(amounts)
    average = total / len(amounts)

    highest = max(expenses, key=lambda e: e.amount)
    lowest = min(expenses, key=lambda e: e.amount)

    print("\nEXPENSE STATISTICS")
    print("-" * 40)
    print(f"Total expenses: {len(expenses)}")
    print(f"Total spent: Rs. {total:.2f}")
    print(f"Average expense: Rs. {average:.2f}")
    print(f"Highest expense: {highest}")
    print(f"Lowest expense: {lowest}")

    return {
        "count": len(expenses),
        "total": total,
        "average": average,
        "highest": highest.amount,
        "lowest": lowest.amount
    }


def expense_chart(expenses):
    totals = defaultdict(float)

    for expense in expenses:
        totals[expense.category] += expense.amount

    print("\nEXPENSE CHART")
    print("-" * 40)

    if not totals:
        print("No data to display.")
        return

    largest = max(totals.values())

    for category, amount in sorted(totals.items()):
        bar_length = int(amount / largest * 20)
        bar = "#" * bar_length
        print(f"{category:12} | {bar} Rs. {amount:.2f}")


def monthly_trend(expenses):
    totals = defaultdict(float)

    for expense in expenses:
        month = expense.date[:7]
        totals[month] += expense.amount

    print("\nMONTHLY SPENDING TREND")
    print("-" * 40)

    for month, amount in sorted(totals.items()):
        print(f"{month}: Rs. {amount:.2f}")

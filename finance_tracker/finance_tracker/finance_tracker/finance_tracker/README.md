
# Personal Finance Tracker

## Overview
Personal Finance Tracker is a Python-based application that helps users record, manage, search, and analyze their daily expenses.

## Features
- Add and view expenses
- Validate expense dates, amounts, and categories
- Store expense data in a JSON file
- Export and import expense data using CSV
- Search expenses by date, category, or description
- Generate monthly expense reports
- View category-wise breakdown and statistics
- Check monthly spending against a budget
- Create and restore data backups
- Handle file-related errors

## Project Structure
```text
week4-finance-tracker/
├── finance_tracker/
│   ├── __init__.py
│   ├── main.py
│   ├── expense.py
│   ├── expense_manager.py
│   ├── file_handler.py
│   ├── reports.py
│   └── utils.py
├── data/
├── tests/
├── requirements.txt
├── README.md
├── .gitignore
└── run.py
```

## Requirements
- Python 3.8 or later
- No external libraries required

## How to Run
Open a terminal in the project folder and run:

```bash
python run.py
```

## Data Storage
Expenses are stored in JSON format. CSV export and import are also supported. Backup files are stored in the data/backup directory.

## Learning Concepts
This project demonstrates Python classes, functions, modules, file handling, JSON, CSV, exception handling, input validation, and report generation.

## Author
Python Developer Intern

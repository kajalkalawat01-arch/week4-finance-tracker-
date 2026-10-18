
import csv
import json
import shutil
from pathlib import Path
from .expense import Expense


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
DATA_FILE = DATA_DIR / "expenses.json"
BACKUP_DIR = DATA_DIR / "backup"
EXPORT_DIR = DATA_DIR / "exports"


def ensure_directories():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)


def save_expenses(expenses):
    ensure_directories()
    temp_file = DATA_FILE.with_suffix(".tmp")

    try:
        data = [expense.to_dict() for expense in expenses]
        with temp_file.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        temp_file.replace(DATA_FILE)
    except (OSError, TypeError, ValueError) as error:
        if temp_file.exists():
            temp_file.unlink()
        raise RuntimeError(f"Could not save expenses: {error}") from error


def load_expenses():
    ensure_directories()

    if not DATA_FILE.exists():
        return []

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, list):
            raise ValueError("Expense data must be a list.")

        return [Expense.from_dict(item) for item in data]

    except (OSError, json.JSONDecodeError, ValueError, TypeError, KeyError) as error:
        raise RuntimeError(f"Could not load expenses: {error}") from error


def export_to_csv(expenses):
    ensure_directories()
    export_file = EXPORT_DIR / "expenses.csv"
    fields = ["date", "amount", "category", "description"]

    try:
        with export_file.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writeheader()
            for expense in expenses:
                writer.writerow(expense.to_dict())
        return export_file
    except OSError as error:
        raise RuntimeError(f"Could not export CSV: {error}") from error


def import_from_csv(file_path):
    imported = []
    fields = {"date", "amount", "category", "description"}

    try:
        with open(file_path, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            if not reader.fieldnames or not fields.issubset(reader.fieldnames):
                raise ValueError("CSV file has missing columns.")

            for row in reader:
                imported.append(Expense.from_dict(row))

        return imported
    except (OSError, csv.Error, ValueError, TypeError, KeyError) as error:
        raise RuntimeError(f"Could not import CSV: {error}") from error


def backup_data():
    ensure_directories()

    if not DATA_FILE.exists():
        save_expenses([])

    backup_file = BACKUP_DIR / "expenses_backup.json"

    try:
        shutil.copy2(DATA_FILE, backup_file)
        return backup_file
    except OSError as error:
        raise RuntimeError(f"Could not back up data: {error}") from error


def restore_backup():
    ensure_directories()
    backup_file = BACKUP_DIR / "expenses_backup.json"

    if not backup_file.exists():
        raise FileNotFoundError("No backup file found.")

    try:
        with backup_file.open("r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, list):
            raise ValueError("Backup data must be a list.")

        for item in data:
            Expense.from_dict(item)

        DATA_FILE.write_text(
            json.dumps(data, indent=4, ensure_ascii=False),
            encoding="utf-8"
        )
    except (OSError, json.JSONDecodeError, ValueError, TypeError, KeyError) as error:
        raise RuntimeError(f"Could not restore backup: {error}") from error
  

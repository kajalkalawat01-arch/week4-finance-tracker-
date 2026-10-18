
import unittest
import tempfile
from pathlib import Path
from unittest.mock import patch

from finance_tracker.expense import Expense
from finance_tracker import file_handler


class TestFileHandler(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)

        self.data_dir = Path(self.temp_dir.name) / "data"
        self.data_file = self.data_dir / "expenses.json"
        self.backup_dir = self.data_dir / "backup"
        self.export_dir = self.data_dir / "exports"

        self.patches = [
            patch.object(file_handler, "DATA_DIR", self.data_dir),
            patch.object(file_handler, "DATA_FILE", self.data_file),
            patch.object(file_handler, "BACKUP_DIR", self.backup_dir),
            patch.object(file_handler, "EXPORT_DIR", self.export_dir),
        ]

        for item in self.patches:
            item.start()
            self.addCleanup(item.stop)

    def test_load_missing_file(self):
        self.assertEqual(file_handler.load_expenses(), [])

    def test_save_and_load(self):
        expense = Expense(
            "2026-10-18", 120, "Food", "Lunch"
        )

        file_handler.save_expenses([expense])
        loaded = file_handler.load_expenses()

        self.assertEqual(len(loaded), 1)
        self.assertEqual(loaded[0].amount, 120)
        self.assertEqual(loaded[0].description, "Lunch")

    def test_csv_export(self):
        expense = Expense(
            "2026-10-18", 80, "Travel", "Bus"
        )

        path = file_handler.export_to_csv([expense])

        self.assertTrue(path.exists())
        self.assertIn("description", path.read_text(encoding="utf-8"))

    def test_backup_and_restore(self):
        original = Expense(
            "2026-10-18", 250, "Shopping", "Shoes"
        )

        file_handler.save_expenses([original])
        file_handler.backup_data()
        file_handler.save_expenses([])

        file_handler.restore_backup()
        loaded = file_handler.load_expenses()

        self.assertEqual(len(loaded), 1)
        self.assertEqual(loaded[0].description, "Shoes")


if __name__ == "__main__":
    unittest.main()
  

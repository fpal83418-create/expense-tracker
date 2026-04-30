`python
import unittest
import os
import json
from tracker import ExpenseTracker, DATA_FILE


class TestExpenseTracker(unittest.TestCase):
    def setUp(self):
        self.tracker = ExpenseTracker()
        self.tracker.expenses = []
        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)

    def tearDown(self):
        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)

    def test_add_valid_expense(self):
        success, msg = self.tracker.add_expense("500", "Еда", "2025-01-15")
        self.assertTrue(success)
        self.assertEqual(len(self.tracker.expenses), 1)

    def test_add_negative_amount(self):
        success, msg = self.tracker.add_expense("-100", "Еда", "2025-01-15")
        self.assertFalse(success)

    def test_add_invalid_date(self):
        success, msg = self.tracker.add_expense("100", "Еда", "15-01-2025")
        self.assertFalse(success)

    def test_add_boundary_date(self):
        success, msg = self.tracker.add_expense("100", "Еда", "2025-12-31")
        self.assertTrue(success)

    def test_get_total_by_period(self):
        self.tracker.add_expense("200", "Еда", "2025-01-10")
        self.tracker.add_expense("300", "Транспорт", "2025-01-20")
        total = self.tracker.get_total_by_period("2025-01-01", "2025-01-15")
        self.assertEqual(total, 200)

    def test_filter_by_category(self):
        self.tracker.add_expense("200", "Еда", "2025-01-10")
        self.tracker.add_expense("300", "Транспорт", "2025-01-20")
        result = self.tracker.filter_by_category("Еда")
        self.assertEqual(len(result), 1)

    def test_filter_by_date_range(self):
        self.tracker.add_expense("200", "Еда", "2025-01-10")
        self.tracker.add_expense("300", "Транспорт", "2025-02-20")
        result = self.tracker.filter_by_date_range("2025-01-01", "2025-01-31")
        self.assertEqual(len(result), 1)

    def test_save_and_load(self):
        self.tracker.add_expense("500", "Еда", "2025-01-15")
18:31
self.assertTrue(os.path.exists(DATA_FILE))

        new_tracker = ExpenseTracker()
        self.assertEqual(len(new_tracker.expenses), 1)


if __name__ == "__main__":
    unittest.main()

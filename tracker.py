python
import json
import os
from datetime import datetime

DATA_FILE = "expenses.json"


class ExpenseTracker:
    def __init__(self):
        self.expenses = []
        self.load_data()

    def load_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    self.expenses = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                self.expenses = []
        else:
            self.expenses = []

    def save_data(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.expenses, f, indent=4, ensure_ascii=False)

    def add_expense(self, amount, category, date_str):
        if not self._validate_amount(amount):
            return False, "Сумма должна быть положительным числом."
        if not self._validate_date(date_str):
            return False, "Дата должна быть в формате ГГГГ-ММ-ДД."

        expense = {
            "id": len(self.expenses) + 1,
            "amount": float(amount),
            "category": category.strip(),
            "date": date_str.strip()
        }
        self.expenses.append(expense)
        self.save_data()
        return True, "Расход добавлен."

    def delete_expense(self, expense_id):
        self.expenses = [e for e in self.expenses if e["id"] != expense_id]
        self.save_data()

    def get_all_expenses(self):
        return self.expenses

    def get_total_by_period(self, start_date, end_date):
        try:
            start = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            return None

        total = 0
        for e in self.expenses:
            try:
                d = datetime.strptime(e["date"], "%Y-%m-%d")
                if start <= d <= end:
                    total += e["amount"]
            except ValueError:
                continue
        return total

    def filter_by_category(self, category):
        return [e for e in self.expenses if e["category"].lower() == category.lower()]

    def filter_by_date_range(self, start_date, end_date):
        try:
            start = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            return []

        result = []
        for e in self.expenses:
            try:
                d = datetime.strptime(e["date"], "%Y-%m-%d")
                if start <= d <= end:
                    result.append(e)
            except ValueError:
                continue
        return result

    def _validate_amount(self, value):
        try:
            return float(value) > 0
        except (ValueError, TypeError):
            return False

    def _validate_date(self, date_str):
        try:
            datetime.strptime(date_str.strip(), "%Y-%m-%d")
            return True
        except (ValueError, TypeError):
            return False

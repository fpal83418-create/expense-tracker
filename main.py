import tkinter as tk
from tkinter import ttk, messagebox
from tracker import ExpenseTracker


class App:
    def __init__(self, root):
        self.tracker = ExpenseTracker()
        self.root = root
        self.root.title("Expense Tracker")
        self.root.geometry("900x600")
        
        # -------- Верхняя панель ввода --------
        input_frame = ttk.LabelFrame(root, text="Добавить расход", padding=10)
        input_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(input_frame, text="Сумма:").grid(row=0, column=0, sticky="w", padx=5)
        self.amount_entry = ttk.Entry(input_frame, width=15)
        self.amount_entry.grid(row=0, column=1, padx=5)

        ttk.Label(input_frame, text="Категория:").grid(row=0, column=2, sticky="w", padx=5)
        self.category_combo = ttk.Combobox(input_frame, values=["Еда", "Транспорт", "Развлечения", "Здоровье", "Одежда", "Другое"], width=15)
        self.category_combo.grid(row=0, column=3, padx=5)
        self.category_combo.set("Еда")

        ttk.Label(input_frame, text="Дата (ГГГГ-ММ-ДД):").grid(row=0, column=4, sticky="w", padx=5)
        self.date_entry = ttk.Entry(input_frame, width=15)
        self.date_entry.grid(row=0, column=5, padx=5)
        self.date_entry.insert(0, "2024-01-01")  # Значение по умолчанию

        ttk.Button(input_frame, text="Добавить расход", command=self.add_expense).grid(row=0, column=6, padx=10)

        # -------- Панель фильтрации и подсчёта --------
        filter_frame = ttk.LabelFrame(root, text="Фильтрация и подсчёт за период", padding=10)
        filter_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(filter_frame, text="Категория:").grid(row=0, column=0, sticky="w", padx=5)
        self.filter_category = ttk.Combobox(filter_frame, values=["Все", "Еда", "Транспорт", "Развлечения", "Здоровье", "Одежда", "Другое"], width=15)
        self.filter_category.grid(row=0, column=1, padx=5)
        self.filter_category.set("Все")

        ttk.Label(filter_frame, text="С даты:").grid(row=0, column=2, sticky="w", padx=5)
        self.start_date_entry = ttk.Entry(filter_frame, width=12)
        self.start_date_entry.grid(row=0, column=3, padx=5)

        ttk.Label(filter_frame, text="По дату:").grid(row=0, column=4, sticky="w", padx=5)
        self.end_date_entry = ttk.Entry(filter_frame, width=12)
        self.end_date_entry.grid(row=0, column=5, padx=5)

        ttk.Button(filter_frame, text="Фильтровать", command=self.filter_expenses).grid(row=0, column=6, padx=5)
        ttk.Button(filter_frame, text="Подсчитать сумму", command=self.calculate_total).grid(row=0, column=7, padx=5)
        ttk.Button(filter_frame, text="Показать всё", command=self.refresh_table).grid(row=0, column=8, padx=5)

        # -------- Таблица расходов --------
        table_frame = ttk.Frame(root)
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)

        columns = ("id", "amount", "category", "date")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        self.tree.heading("id", text="ID")
        self.tree.heading("amount", text="Сумма (руб.)")
        self.tree.heading("category", text="Категория")
        self.tree.heading("date", text="Дата")
        self.tree.column("id", width=50)
        self.tree.column("amount", width=100)
        self.tree.column("category", width=150)
        self.tree.column("date", width=120)
        self.tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Кнопка удаления
        button_frame = ttk.Frame(root)
        button_frame.pack(pady=10)
        ttk.Button(button_frame, text="Удалить выбранный расход", command=self.delete_expense).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Очистить фильтры", command=self.clear_filters).pack(side="left", padx=5)

        # Загрузка данных при старте
        self.refresh_table()

    # ---------- Методы ----------
    def add_expense(self):
        amount = self.amount_entry.get().strip()
        category = self.category_combo.get().strip()
        date = self.date_entry.get().strip()

        if not amount:
            messagebox.showerror("Ошибка", "Введите сумму!")
            return
            
        if not date:
            messagebox.showerror("Ошибка", "Введите дату!")
            return

        success, msg = self.tracker.add_expense(amount, category, date)
        if success:
            self.amount_entry.delete(0, tk.END)
            self.date_entry.delete(0, tk.END)
            self.date_entry.insert(0, "2024-01-01")  # Восстанавливаем значение по умолчанию
            self.refresh_table()
            messagebox.showinfo("Успех", "Расход успешно добавлен!")
        else:
            messagebox.showerror("Ошибка", msg)

    def refresh_table(self):
        # Очищаем таблицу
        for row in self.tree.get_children():
            self.tree.delete(row)
        # Загружаем все расходы
        for e in self.tracker.get_all_expenses():
            self.tree.insert("", "end", values=(e["id"], e["amount"], e["category"], e["date"]))

    def filter_expenses(self):
        category = self.filter_category.get().strip()
        start = self.start_date_entry.get().strip()
        end = self.end_date_entry.get().strip()

        expenses = self.tracker.get_all_expenses()
        
        # Применяем фильтр по категории
        if category != "Все":
            expenses = self.tracker.filter_by_category(category)
        
        # Применяем фильтр по датам
        if start and end:
            date_filtered = self.tracker.filter_by_date_range(start, end)
            # Пересекаем результаты, если есть оба фильтра
            if category != "Все":
                expenses = [e for e in expenses if e in date_filtered]
            else:
                expenses = date_filtered
        elif start or end:
            messagebox.showwarning("Предупреждение", "Для фильтрации по датам нужно указать обе даты!")
            return

        # Очищаем таблицу и показываем отфильтрованные результаты
        for row in self.tree.get_children():
            self.tree.delete(row)
        for e in expenses:
            self.tree.insert("", "end", values=(e["id"], e["amount"], e["category"], e["date"]))

    def clear_filters(self):
        """Очищает все фильтры"""
        self.filter_category.set("Все")
        self.start_date_entry.delete(0, tk.END)
        self.end_date_entry.delete(0, tk.END)
        self.refresh_table()

    def calculate_total(self):
        start = self.start_date_entry.get().strip()
        end = self.end_date_entry.get().strip()
        
        if not start or not end:
            messagebox.showwarning("Предупреждение", "Введите начальную и конечную дату для подсчёта.")
            return
        
        total = self.tracker.get_total_by_period(start, end)
        if total is None:
            messagebox.showerror("Ошибка", "Неверный формат даты. Используйте ГГГГ-ММ-ДД")
        else:
            messagebox.showinfo("Сумма за период", f"Общая сумма расходов: {total:.2f} руб.")

    def delete_expense(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите запись для удаления.")
            return
        
        # Подтверждение удаления
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить выбранный расход?"):
            item = self.tree.item(selected[0])
            expense_id = item["values"][0]
            self.tracker.delete_expense(expense_id)
            self.refresh_table()
            messagebox.showinfo("Успех", "Расход успешно удален!")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()

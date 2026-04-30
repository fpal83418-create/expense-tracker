import tkinter as tk
from tkinter import ttk, messagebox
from book_tracker import BookTracker
from datetime import datetime


class BookTrackerApp:
    def __init__(self, root):
        self.tracker = BookTracker()
        self.root = root
        self.root.title("Book Tracker - Трекер прочитанных книг")
        self.root.geometry("1000x700")
        
        # Установка иконки (опционально)
        try:
            self.root.iconbitmap('icon.ico')
        except:
            pass
        
        # Стилизация
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Title.TLabel", font=("Arial", 14, "bold"))
        style.configure("Header.TLabel", font=("Arial", 11, "bold"))
        
        # Заголовок
        title_frame = ttk.Frame(root)
        title_frame.pack(fill="x", padx=10, pady=10)
        title_label = ttk.Label(title_frame, text="📚 Трекер прочитанных книг", style="Title.TLabel")
        title_label.pack()
        
        # -------- Форма добавления книги --------
        add_frame = ttk.LabelFrame(root, text="➕ Добавить новую книгу", padding=15)
        add_frame.pack(fill="x", padx=10, pady=5)
        
        # Поля ввода
        # Название книги
        ttk.Label(add_frame, text="Название книги:", font=("Arial", 10)).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.title_entry = ttk.Entry(add_frame, width=30, font=("Arial", 10))
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Автор
        ttk.Label(add_frame, text="Автор:", font=("Arial", 10)).grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.author_entry = ttk.Entry(add_frame, width=25, font=("Arial", 10))
        self.author_entry.grid(row=0, column=3, padx=5, pady=5)
        
        # Жанр
        ttk.Label(add_frame, text="Жанр:", font=("Arial", 10)).grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.genre_combo = ttk.Combobox(add_frame, values=[
            "Роман", "Детектив", "Фантастика", "Фэнтези", "Научная литература",
            "Биография", "Поэзия", "Драма", "Комедия", "Приключения", 
            "Триллер", "Ужасы", "Историческая", "Другое"
        ], width=27, font=("Arial", 10))
        self.genre_combo.grid(row=1, column=1, padx=5, pady=5)
        self.genre_combo.set("Роман")
        
        # Количество страниц
        ttk.Label(add_frame, text="Количество страниц:", font=("Arial", 10)).grid(row=1, column=2, sticky="w", padx=5, pady=5)
        self.pages_entry = ttk.Entry(add_frame, width=15, font=("Arial", 10))
        self.pages_entry.grid(row=1, column=3, padx=5, pady=5)
        
        # Кнопка добавления
        ttk.Button(add_frame, text="📖 Добавить книгу", command=self.add_book, width=20).grid(row=1, column=4, padx=20, pady=5)
        
        # -------- Панель фильтрации --------
        filter_frame = ttk.LabelFrame(root, text="🔍 Фильтрация книг", padding=15)
        filter_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(filter_frame, text="Фильтр по жанру:", font=("Arial", 10)).grid(row=0, column=0, sticky="w", padx=5)
        self.filter_genre = ttk.Combobox(filter_frame, values=["Все жанры", "Роман", "Детектив", "Фантастика", "Фэнтези", "Научная литература", "Биография", "Поэзия", "Драма", "Комедия", "Приключения", "Триллер", "Ужасы", "Историческая", "Другое"], width=25)
        self.filter_genre.grid(row=0, column=1, padx=5)
        self.filter_genre.set("Все жанры")
        
        ttk.Label(filter_frame, text="Фильтр по страницам (>):", font=("Arial", 10)).grid(row=0, column=2, sticky="w", padx=5)
        self.filter_pages = ttk.Entry(filter_frame, width=10, font=("Arial", 10))
        self.filter_pages.grid(row=0, column=3, padx=5)
        
        # Кнопки фильтрации
        button_filter_frame = ttk.Frame(filter_frame)
        button_filter_frame.grid(row=0, column=4, columnspan=3, padx=10)
        
        ttk.Button(button_filter_frame, text="🔍 Применить фильтр", command=self.filter_books, width=18).pack(side="left", padx=2)
        ttk.Button(button_filter_frame, text="🔄 Сбросить фильтры", command=self.clear_filters, width=18).pack(side="left", padx=2)
        ttk.Button(button_filter_frame, text="📋 Показать все", command=self.refresh_table, width=15).pack(side="left", padx=2)
        
        # -------- Таблица с книгами --------
        table_frame = ttk.Frame(root)
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Создание таблицы
        columns = ("id", "title", "author", "genre", "pages")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        
        # Настройка заголовков
        self.tree.heading("id", text="ID")
        self.tree.heading("title", text="Название книги")
        self.tree.heading("author", text="Автор")
        self.tree.heading("genre", text="Жанр")
        self.tree.heading("pages", text="Страниц")
        
        # Настройка ширины колонок
        self.tree.column("id", width=50, anchor="center")
        self.tree.column("title", width=300, anchor="w")
        self.tree.column("author", width=200, anchor="w")
        self.tree.column("genre", width=150, anchor="center")
        self.tree.column("pages", width=100, anchor="center")
        
        # Скроллбары
        scrollbar_y = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        scrollbar_x = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x.pack(side="bottom", fill="x")
        
        # Нижняя панель с кнопками управления
        control_frame = ttk.Frame(root)
        control_frame.pack(pady=10)
        
        ttk.Button(control_frame, text="🗑 Удалить выбранную книгу", command=self.delete_book, width=22).pack(side="left", padx=5)
        ttk.Button(control_frame, text="📊 Статистика", command=self.show_statistics, width=15).pack(side="left", padx=5)
        ttk.Button(control_frame, text="💾 Сохранить данные", command=self.save_data, width=15).pack(side="left", padx=5)
        
        # Статус бар
        self.status_bar = ttk.Label(root, text="✅ Готово | Всего книг: 0", relief="sunken", anchor="w")
        self.status_bar.pack(side="bottom", fill="x", padx=10, pady=5)
        
        # Привязка клавиш
        self.root.bind('<Delete>', lambda e: self.delete_book())
        self.root.bind('<Control-d>', lambda e: self.delete_book())
        self.root.bind('<F5>', lambda e: self.refresh_table())
        
        # Загрузка данных
        self.refresh_table()
    
    def add_book(self):
        """Добавление новой книги"""
        title = self.title_entry.get()
        author = self.author_entry.get()
        genre = self.genre_combo.get()
        pages = self.pages_entry.get()
        
        # Валидация данных
        is_valid, result = self.tracker.validate_book(title, author, genre, pages)
        
        if not is_valid:
            messagebox.showerror("Ошибка ввода", result)
            self.status_bar.config(text=f"❌ {result}")
            return
        
        pages_num = result
        
        # Добавление книги
        success, msg = self.tracker.add_book(title, author, genre, pages_num)
        
        if success:
            # Очистка полей
            self.title_entry.delete(0, tk.END)
            self.author_entry.delete(0, tk.END)
            self.pages_entry.delete(0, tk.END)
            
            # Обновление таблицы
            self.refresh_table()
            self.status_bar.config(text=f"✅ {msg}")
            messagebox.showinfo("Успех", msg)
        else:
            messagebox.showerror("Ошибка", msg)
            self.status_bar.config(text=f"❌ {msg}")
    
    def refresh_table(self):
        """Обновление таблицы со всеми книгами"""
        # Очистка таблицы
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        # Заполнение таблицы
        for book in self.tracker.get_all_books():
            self.tree.insert("", "end", values=(
                book["id"],
                book["title"],
                book["author"],
                book["genre"],
                f"{book['pages']} стр."
            ))
        
        # Обновление статуса
        total_books = len(self.tracker.get_all_books())
        total_pages = sum(book["pages"] for book in self.tracker.get_all_books())
        self.status_bar.config(text=f"✅ Готово | Всего книг: {total_books} | Всего страниц: {total_pages}")
    
    def filter_books(self):
        """Фильтрация книг"""
        genre = self.filter_genre.get()
        pages_filter = self.filter_pages.get().strip()
        
        # Валидация фильтра по страницам
        min_pages = 0
        if pages_filter:
            try:
                min_pages = int(pages_filter)
                if min_pages < 0:
                    messagebox.showwarning("Предупреждение", "Количество страниц должно быть положительным числом!")
                    return
            except ValueError:
                messagebox.showerror("Ошибка", "Введите корректное число для фильтрации по страницам!")
                return
        
        # Применение фильтров
        if genre == "Все жанры" and min_pages == 0:
            filtered_books = self.tracker.get_all_books()
        elif min_pages == 0:
            filtered_books = self.tracker.filter_by_genre(genre)
        elif genre == "Все жанры":
            filtered_books = self.tracker.filter_by_pages(min_pages)
        else:
            filtered_books = self.tracker.filter_by_genre_and_pages(genre, min_pages)
        
        # Обновление таблицы
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        for book in filtered_books:
            self.tree.insert("", "end", values=(
                book["id"],
                book["title"],
                book["author"],
                book["genre"],
                f"{book['pages']} стр."
            ))
        
        # Обновление статуса
        total_pages_filtered = sum(book["pages"] for book in filtered_books)
        self.status_bar.config(text=f"🔍 Отфильтровано: {len(filtered_books)} книг | Всего страниц: {total_pages_filtered}")
    
    def clear_filters(self):
        """Сброс всех фильтров"""
        self.filter_genre.set("Все жанры")
        self.filter_pages.delete(0, tk.END)
        self.refresh_table()
        self.status_bar.config(text="🔄 Фильтры сброшены")
    
    def delete_book(self):
        """Удаление выбранной книги"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите книгу для удаления!")
            return
        
        # Информация о книге для подтверждения
        item = self.tree.item(selected[0])
        book_title = item["values"][1]
        book_author = item["values"][2]
        
        # Подтверждение удаления
        if messagebox.askyesno("Подтверждение удаления", 
                               f"Вы уверены, что хотите удалить книгу:\n\n"
                               f"📖 {book_title}\n✍️ {book_author}\n\n"
                               f"Это действие нельзя отменить!"):
            book_id = item["values"][0]
            
            if self.tracker.delete_book(book_id):
                self.refresh_table()
                self.status_bar.config(text=f"✅ Книга '{book_title}' удалена")
                messagebox.showinfo("Успех", "Книга успешно удалена!")
            else:
                messagebox.showerror("Ошибка", "Не удалось удалить книгу!")
    
    def save_data(self):
        """Принудительное сохранение данных"""
        if self.tracker.save_books():
            self.status_bar.config(text="✅ Данные успешно сохранены")
            messagebox.showinfo("Успех", "Данные сохранены в файл books.json")
        else:
            self.status_bar.config(text="❌ Ошибка при сохранении данных")
            messagebox.showerror("Ошибка", "Не удалось сохранить данные!")
    
    def show_statistics(self):
        """Показывает статистику по книгам"""
        stats = self.tracker.get_statistics()
        
        if not stats:
            messagebox.showinfo("Статистика", "Нет данных для отображения статистики")
            return
        
        # Формирование сообщения со статистикой
        stats_text = "📊 СТАТИСТИКА ПРОЧИТАННЫХ КНИГ\n"
        stats_text += "=" * 40 + "\n\n"
        stats_text += f"📚 Всего книг: {stats['total_books']}\n"
        stats_text += f"📖 Всего страниц: {stats['total_pages']}\n"
        stats_text += f"📈 Среднее количество страниц: {stats['avg_pages']:.1f}\n\n"
        
        stats_text += "🎭 Распределение по жанрам:\n"
        stats_text += "-" * 30 + "\n"
        
        for genre, count in sorted(stats['genres_count'].items(), key=lambda x: x[1], reverse=True):
            percentage = (count / stats['total_books']) * 100
            stats_text += f"  • {genre}: {count} книг ({percentage:.1f}%)\n"
        
        messagebox.showinfo("Статистика книг", stats_text)


if __name__ == "__main__":
    root = tk.Tk()
    app = BookTrackerApp(root)
    root.mainloop()
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

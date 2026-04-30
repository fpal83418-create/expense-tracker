import json
import os
from typing import List, Dict, Optional


class BookTracker:
    """Класс для управления списком прочитанных книг"""
    
    def __init__(self, data_file="books.json"):
        self.data_file = data_file
        self.books = []
        self.load_books()
    
    def load_books(self):
        """Загружает данные из JSON файла"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    self.books = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                self.books = []
        else:
            self.books = []
    
    def save_books(self):
        """Сохраняет данные в JSON файл"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.books, f, ensure_ascii=False, indent=4)
            return True
        except Exception:
            return False
    
    def validate_book(self, title: str, author: str, genre: str, pages: str) -> tuple:
        """Проверяет корректность ввода данных"""
        # Проверка на пустые поля
        if not title or not title.strip():
            return False, "Название книги не может быть пустым!"
        
        if not author or not author.strip():
            return False, "Автор не может быть пустым!"
        
        if not genre or not genre.strip():
            return False, "Жанр не может быть пустым!"
        
        if not pages or not pages.strip():
            return False, "Количество страниц не может быть пустым!"
        
        # Проверка количества страниц (должно быть числом)
        try:
            pages_num = int(pages)
            if pages_num <= 0:
                return False, "Количество страниц должно быть положительным числом!"
        except ValueError:
            return False, "Количество страниц должно быть целым числом!"
        
        return True, pages_num
    
    def add_book(self, title: str, author: str, genre: str, pages: int) -> tuple:
        """Добавляет новую книгу"""
        book = {
            "id": len(self.books) + 1,
            "title": title.strip(),
            "author": author.strip(),
            "genre": genre.strip(),
            "pages": pages
        }
        
        self.books.append(book)
        if self.save_books():
            return True, "Книга успешно добавлена!"
        return False, "Ошибка при сохранении данных"
    
    def get_all_books(self) -> List[Dict]:
        """Возвращает все книги"""
        return self.books
    
    def filter_by_genre(self, genre: str) -> List[Dict]:
        """Фильтрует книги по жанру"""
        if genre == "Все жанры":
            return self.books
        return [b for b in self.books if b["genre"] == genre]
    
    def filter_by_pages(self, min_pages: int) -> List[Dict]:
        """Фильтрует книги по количеству страниц (больше указанного)"""
        return [b for b in self.books if b["pages"] > min_pages]
    
    def filter_by_genre_and_pages(self, genre: str, min_pages: int) -> List[Dict]:
        """Фильтрует книги по жанру и количеству страниц"""
        result = self.books
        
        if genre != "Все жанры":
            result = [b for b in result if b["genre"] == genre]
        
        if min_pages > 0:
            result = [b for b in result if b["pages"] > min_pages]
        
        return result
    
    def delete_book(self, book_id: int) -> bool:
        """Удаляет книгу по ID"""
        for i, book in enumerate(self.books):
            if book["id"] == book_id:
                self.books.pop(i)
                # Перенумеровываем ID
                for idx, book in enumerate(self.books, 1):
                    book["id"] = idx
                self.save_books()
                return True
        return False
    
    def get_statistics(self) -> Dict:
        """Получает статистику по книгам"""
        if not self.books:
            return {}
        
        # Статистика по жанрам
        genres_count = {}
        for book in self.books:
            genre = book["genre"]
            genres_count[genre] = genres_count.get(genre, 0) + 1
        
        total_pages = sum(book["pages"] for book in self.books)
        avg_pages = total_pages / len(self.books)
        
        return {
            "total_books": len(self.books),
            "total_pages": total_pages,
            "avg_pages": avg_pages,
            "genres_count": genres_count
        }
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

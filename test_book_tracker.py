import unittest
import os
import json
from book_tracker import BookTracker


class TestBookTracker(unittest.TestCase):
    """Тесты для класса BookTracker"""
    
    def setUp(self):
        """Подготовка перед каждым тестом"""
        self.data_file = "test_books.json"
        self.tracker = BookTracker(data_file=self.data_file)
        self.tracker.books = []
        if os.path.exists(self.data_file):
            os.remove(self.data_file)
    
    def tearDown(self):
        """Очистка после каждого теста"""
        if os.path.exists(self.data_file):
            os.remove(self.data_file)
    
    # ========== Тесты валидации ==========
    
    def test_validate_valid_book(self):
        """Тест: проверка корректной книги"""
        is_valid, result = self.tracker.validate_book("Война и мир", "Лев Толстой", "Роман", "1225")
        self.assertTrue(is_valid)
        self.assertEqual(result, 1225)
    
    def test_validate_empty_title(self):
        """Тест: проверка пустого названия"""
        is_valid, result = self.tracker.validate_book("", "Лев Толстой", "Роман", "1225")
        self.assertFalse(is_valid)
        self.assertIn("Название", result)
    
    def test_validate_empty_author(self):
        """Тест: проверка пустого автора"""
        is_valid, result = self.tracker.validate_book("Война и мир", "", "Роман", "1225")
        self.assertFalse(is_valid)
        self.assertIn("Автор", result)
    
    def test_validate_empty_genre(self):
        """Тест: проверка пустого жанра"""
        is_valid, result = self.tracker.validate_book("Война и мир", "Лев Толстой", "", "1225")
        self.assertFalse(is_valid)
        self.assertIn("Жанр", result)
    
    def test_validate_empty_pages(self):
        """Тест: проверка пустого количества страниц"""
        is_valid, result = self.tracker.validate_book("Война и мир", "Лев Толстой", "Роман", "")
        self.assertFalse(is_valid)
        self.assertIn("не может быть пустым", result)
    
    def test_validate_pages_not_number(self):
        """Тест: проверка, что страницы - число"""
        is_valid, result = self.tracker.validate_book("Война и мир", "Лев Толстой", "Роман", "abc")
        self.assertFalse(is_valid)
        self.assertIn("целым числом", result)
    
    def test_validate_pages_negative(self):
        """Тест: проверка отрицательного количества страниц"""
        is_valid, result = self.tracker.validate_book("Война и мир", "Лев Толстой", "Роман", "-100")
        self.assertFalse(is_valid)
        self.assertIn("положительным", result)
    
    def test_validate_pages_zero(self):
        """Тест: проверка нулевого количества страниц"""
        is_valid, result = self.tracker.validate_book("Война и мир", "Лев Толстой", "Роман", "0")
        self.assertFalse(is_valid)
        self.assertIn("положительным", result)
    
    # ========== Тесты добавления книг ==========
    
    def test_add_valid_book(self):
        """Тест: добавление корректной книги"""
        success, msg = self.tracker.add_book("Война и мир", "Лев Толстой", "Роман", 1225)
        self.assertTrue(success)
        self.assertEqual(len(self.tracker.books), 1)
        self.assertEqual(self.tracker.books[0]["title"], "Война и мир")
        self.assertEqual(self.tracker.books[0]["author"], "Лев Толстой")
        self.assertEqual(self.tracker.books[0]["genre"], "Роман")
        self.assertEqual(self.tracker.books[0]["pages"], 1225)
    
    def test_add_multiple_books(self):
        """Тест: добавление нескольких книг"""
        self.tracker.add_book("Война и мир", "Лев Толстой", "Роман", 1225)
        self.tracker.add_book("Преступление и наказание", "Федор Достоевский", "Роман", 672)
        self.assertEqual(len(self.tracker.books), 2)
        self.assertEqual(self.tracker.books[1]["id"], 2)
    
    def test_add_book_with_whitespace(self):
        """Тест: добавление книги с пробелами в полях"""
        success, msg = self.tracker.add_book("  Война и мир  ", "  Лев Толстой  ", "  Роман  ", 1225)
        self.assertTrue(success)
        self.assertEqual(self.tracker.books[0]["title"], "Война и мир")
        self.assertEqual(self.tracker.books[0]["author"], "Лев Толстой")
    
    # ========== Тесты фильтрации ==========
    
    def test_filter_by_genre(self):
        """Тест: фильтрация по жанру"""
        self.tracker.add_book("Война и мир", "Лев Толстой", "Роман", 1225)
        self.tracker.add_book("Метро 2033", "Дмитрий Глуховский", "Фантастика", 384)
        self.tracker.add_book("Идиот", "Федор Достоевский", "Роман", 672)
        
        result = self.tracker.filter_by_genre("Роман")
        self.assertEqual(len(result), 2)
        self.assertTrue(all(book["genre"] == "Роман" for book in result))
    
    def test_filter_by_genre_all(self):
        """Тест: фильтрация по всем жанрам"""
        self.tracker.add_book("Война и мир", "Лев Толстой", "Роман", 1225)
        self.tracker.add_book("Метро 2033", "Дмитрий Глуховский", "Фантастика", 384)
        
        result = self.tracker.filter_by_genre("Все жанры")
        self.assertEqual(len(result), 2)
    
    def test_filter_by_pages(self):
        """Тест: фильтрация по количеству страниц (> N)"""
        self.tracker.add_book("Война и мир", "Лев Толстой", "Роман", 1225)
        self.tracker.add_book("Метро 2033", "Дмитрий Глуховский", "Фантастика", 384)
        self.tracker.add_book("Короткая книга", "Тест", "Поэзия", 100)
        
        result = self.tracker.filter_by_pages(400)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["title"], "Война и мир")
    
    def test_filter_by_pages_boundary(self):
        """Тест: фильтрация по граничному значению страниц"""
        self.tracker.add_book("Книга 300 стр", "Автор", "Жанр", 300)
        self.tracker.add_book("Книга 301 стр", "Автор", "Жанр", 301)
        
        result = self.tracker.filter_by_pages(300)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["pages"], 301)
    
    def test_filter_by_genre_and_pages(self):
        """Тест: комбинированная фильтрация по жанру и страницам"""
        self.tracker.add_book("Война и мир", "Лев Толстой", "Роман", 1225)
        self.tracker.add_book("Идиот", "Федор Достоевский", "Роман", 672)
        self.tracker.add_book("Метро 2033", "Дмитрий Глуховский", "Фантастика", 384)
        
        result = self.tracker.filter_by_genre_and_pages("Роман", 1000)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["title"], "Война и мир")
    
    # ========== Тесты удаления ==========
    
    def test_delete_book(self):
        """Тест: удаление книги"""
        self.tracker.add_book("Война и мир", "Лев Толстой", "Роман", 1225)
        self.tracker.add_book("Метро 2033", "Дмитрий Глуховский", "Фантастика", 384)
        
        result = self.tracker.delete_book(1)
        self.assertTrue(result)
        self.assertEqual(len(self.tracker.books), 1)
        self.assertEqual(self.tracker.books[0]["id"], 1)
        self.assertEqual(self.tracker.books[0]["title"], "Метро 2033")
    
    def test_delete_nonexistent_book(self):
        """Тест: удаление несуществующей книги"""
        self.tracker.add_book("Война и мир", "Лев Толстой", "Роман", 1225)
        
        result = self.tracker.delete_book(999)
        self.assertFalse(result)
        self.assertEqual(len(self.tracker.books), 1)
    
    def test_delete_and_reindex_ids(self):
        """Тест: проверка перенумерации ID после удаления"""
        self.tracker.add_book("Книга 1", "Автор 1", "Жанр 1", 100)
        self.tracker.add_book("Книга 2", "Автор 2", "Жанр 2", 200)
        self.tracker.add_book("Книга 3", "Автор 3", "Жанр 3", 300)
        
        self.tracker.delete_book(2)
        
        self.assertEqual(self.tracker.books[0]["id"], 1)
        self.assertEqual(self.tracker.books[1]["id"], 2)
        self.assertEqual(self.tracker.books[1]["title"], "Книга 3")
    
    # ========== Тесты сохранения и загрузки ==========
    
    def test_save_books(self):
        """Тест: сохранение книг в файл"""
        self.tracker.add_book("Война и мир", "Лев Толстой", "Роман", 1225)
        self.tracker.save_books()
        
        self.assertTrue(os.path.exists(self.data_file))
        
        with open(self.data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["title"], "Война и мир")
    
    def test_load_books(self):
        """Тест: загрузка книг из файла"""
        self.tracker.add_book("Война и мир", "Лев Толстой", "Роман", 1225)
        self.tracker.save_books()
        
        new_tracker = BookTracker(data_file=self.data_file)
        self.assertEqual(len(new_tracker.books), 1)
        self.assertEqual(new_tracker.books[0]["title"], "Война и мир")
    
    def test_load_from_nonexistent_file(self):
        """Тест: загрузка из несуществующего файла"""
        if os.path.exists(self.data_file):
            os.remove(self.data_file)
        
        tracker = BookTracker(data_file=self.data_file)
        self.assertEqual(len(tracker.books), 0)
    
    # ========== Тесты статистики ==========
    
    def test_get_statistics_empty(self):
        """Тест: статистика для пустого списка"""
        stats = self.tracker.get_statistics()
        self.assertEqual(stats, {})
    
    def test_get_statistics_with_books(self):
        """Тест: статистика для списка книг"""
        self.tracker.add_book("Война и мир", "Лев Толстой", "Роман", 1225)
        self.tracker.add_book("Метро 2033", "Дмитрий Глуховский", "Фантастика", 384)
        self.tracker.add_book("Идиот", "Федор Достоевский", "Роман", 672)
        
        stats = self.tracker.get_statistics()
        
        self.assertEqual(stats["total_books"], 3)
        self.assertEqual(stats["total_pages"], 1225 + 384 + 672)
        self.assertAlmostEqual(stats["avg_pages"], (1225 + 384 + 672) / 3)
        self.assertEqual(stats["genres_count"]["Роман"], 2)
        self.assertEqual(stats["genres_count"]["Фантастика"], 1)
    
    # ========== Тесты граничных значений ==========
    
    def test_book_with_max_pages(self):
        """Тест: книга с максимальным количеством страниц"""
        success, msg = self.tracker.add_book("Максимум", "Автор", "Жанр", 999999)
        self.assertTrue(success)
        self.assertEqual(self.tracker.books[0]["pages"], 999999)
    
    def test_book_with_min_pages(self):
        """Тест: книга с минимальным количеством страниц"""
        success, msg = self.tracker.add_book("Минимум", "Автор", "Жанр", 1)
        self.assertTrue(success)
        self.assertEqual(self.tracker.books[0]["pages"], 1)
    
    def test_book_with_very_long_title(self):
        """Тест: книга с очень длинным названием"""
        long_title = "Очень длинное название книги " * 50
        success, msg = self.tracker.add_book(long_title, "Автор", "Жанр", 100)
        self.assertTrue(success)
        self.assertEqual(self.tracker.books[0]["title"], long_title.strip())
    
    def test_filter_by_pages_with_zero(self):
        """Тест: фильтрация по страницам с нулем"""
        self.tracker.add_book("Книга 1", "Автор 1", "Жанр 1", 100)
        self.tracker.add_book("Книга 2", "Автор 2", "Жанр 2", 200)
        
        result = self.tracker.filter_by_pages(0)
        self.assertEqual(len(result), 2)
    
    # ========== Тесты целостности данных ==========
    
    def test_unique_ids(self):
        """Тест: уникальность ID книг"""
        for i in range(10):
            self.tracker.add_book(f"Книга {i}", f"Автор {i}", "Жанр", 100)
        
        ids = [book["id"] for book in self.tracker.books]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(max(ids), 10)
    
    def test_data_persistence(self):
        """Тест: сохранение данных между сессиями"""
        self.tracker.add_book("Война и мир", "Лев Толстой", "Роман", 1225)
        self.tracker.save_books()
        
        # Создаем новый трекер
        new_tracker = BookTracker(data_file=self.data_file)
        self.assertEqual(len(new_tracker.books), 1)
        
        # Добавляем еще одну книгу
        new_tracker.add_book("Метро 2033", "Дмитрий Глуховский", "Фантастика", 384)
        self.assertEqual(len(new_tracker.books), 2)
        
        # Проверяем, что старые данные сохранились
        titles = [book["title"] for book in new_tracker.books]
        self.assertIn("Война и мир", titles)
        self.assertIn("Метро 2033", titles)


if __name__ == "__main__":
    # Запуск с подробным выводом
    unittest.main(verbosity=2)
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

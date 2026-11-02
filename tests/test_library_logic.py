import unittest
import sqlite3
import datetime
from library_logic import (
    validate_book,
    search_books,
    validate_student,
    calculate_overdue,
    issue_book,
    return_book,
    can_delete_book,
    can_delete_student,
)


class ValidateBookTests(unittest.TestCase):
    def test_valid_book_has_no_error(self):
        self.assertIsNone(validate_book("The Alchemist", "Paulo Coelho", "2"))

    def test_title_is_required(self):
        self.assertEqual(
            validate_book("", "Paulo Coelho", "1"),
            "Please enter a book title."
        )

    def test_whitespace_title_is_rejected(self):
        self.assertEqual(
            validate_book("   ", "Paulo Coelho", "1"),
            "Please enter a book title."
        )

    def test_author_is_required(self):
        self.assertEqual(
            validate_book("Clean Code", "", "1"),
            "Please enter the author's name."
        )

    def test_quantity_must_be_positive(self):
        self.assertEqual(
            validate_book("Book", "Author", "0"),
            "Quantity must be at least 1."
        )

    def test_negative_quantity_rejected(self):
        self.assertEqual(
            validate_book("Book", "Author", "-3"),
            "Quantity must be at least 1."
        )

    def test_quantity_must_be_integer(self):
        self.assertEqual(
            validate_book("Book", "Author", "many"),
            "Quantity must be a whole number."
        )


class SearchBooksTests(unittest.TestCase):
    def setUp(self):
        self.books = [
            {"title": "The Alchemist", "author": "Paulo Coelho"},
            {"title": "Pride and Prejudice", "author": "Jane Austen"},
        ]

    def test_search_matches_title_case_insensitively(self):
        self.assertEqual(len(search_books(self.books, "alchemist")), 1)

    def test_search_matches_author(self):
        self.assertEqual(len(search_books(self.books, "JANE")), 1)

    def test_no_match_returns_empty_list(self):
        self.assertEqual(search_books(self.books, "history"), [])

    def test_empty_query_returns_all_books(self):
        self.assertEqual(len(search_books(self.books, "")), 2)


class ValidateStudentTests(unittest.TestCase):
    def test_valid_student(self):
        self.assertIsNone(validate_student("230001", "Alice Smith", "alice@test.edu", "CSE"))

    def test_missing_student_id(self):
        self.assertEqual(validate_student("", "Alice", "alice@test.edu", "CSE"), "Student ID is required.")

    def test_missing_name(self):
        self.assertEqual(validate_student("230001", "", "alice@test.edu", "CSE"), "Student name is required.")

    def test_missing_email(self):
        self.assertEqual(validate_student("230001", "Alice", "", "CSE"), "Student email is required.")

    def test_invalid_email_format(self):
        self.assertEqual(validate_student("230001", "Alice", "invalid-email", "CSE"), "Please enter a valid email address.")

    def test_missing_department(self):
        self.assertEqual(validate_student("230001", "Alice", "alice@test.edu", ""), "Department is required.")


class OverdueCalculationTests(unittest.TestCase):
    def test_not_overdue_when_due_in_future(self):
        future_date = (datetime.date.today() + datetime.timedelta(days=7)).isoformat()
        self.assertFalse(calculate_overdue(future_date))

    def test_overdue_when_due_in_past(self):
        past_date = (datetime.date.today() - datetime.timedelta(days=3)).isoformat()
        self.assertTrue(calculate_overdue(past_date))

    def test_returned_before_due_date_is_not_overdue(self):
        self.assertFalse(calculate_overdue("2026-05-10", return_date_str="2026-05-08"))

    def test_returned_after_due_date_is_overdue(self):
        self.assertTrue(calculate_overdue("2026-05-10", return_date_str="2026-05-12"))


class LibraryTransactionDatabaseTests(unittest.TestCase):
    def setUp(self):
        # Use isolated in-memory database for testing
        self.conn = sqlite3.connect(":memory:")
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA foreign_keys = ON;")
        self.cursor = self.conn.cursor()

        # Schema setup
        self.cursor.execute("""
            CREATE TABLE books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                isbn TEXT,
                quantity INTEGER NOT NULL CHECK(quantity >= 1),
                available INTEGER NOT NULL CHECK(available >= 0)
            )
        """)
        self.cursor.execute("""
            CREATE TABLE students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT NOT NULL UNIQUE,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                department TEXT NOT NULL
            )
        """)
        self.cursor.execute("""
            CREATE TABLE transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id INTEGER NOT NULL,
                student_id TEXT NOT NULL,
                issue_date TEXT NOT NULL,
                due_date TEXT NOT NULL,
                return_date TEXT,
                status TEXT NOT NULL DEFAULT 'ISSUED',
                FOREIGN KEY (book_id) REFERENCES books (id),
                FOREIGN KEY (student_id) REFERENCES students (student_id)
            )
        """)
        self.conn.commit()

        # Seed test data
        self.cursor.execute("INSERT INTO books (title, author, isbn, quantity, available) VALUES ('Design Patterns', 'GoF', '123', 2, 2)")
        self.cursor.execute("INSERT INTO students (student_id, name, email, department) VALUES ('S101', 'Bob Martin', 'bob@test.com', 'CSE')")
        self.conn.commit()

    def tearDown(self):
        self.conn.close()

    def test_issue_book_decrements_available_copies(self):
        success, msg = issue_book(self.conn, 1, 'S101', '2026-05-01', '2026-05-15')
        self.assertTrue(success)

        book = self.conn.execute("SELECT available FROM books WHERE id = 1").fetchone()
        self.assertEqual(book['available'], 1)

        tx = self.conn.execute("SELECT * FROM transactions WHERE book_id = 1").fetchone()
        self.assertIsNotNone(tx)
        self.assertEqual(tx['status'], 'ISSUED')

    def test_issue_book_fails_when_no_copies_available(self):
        # Issue both copies
        issue_book(self.conn, 1, 'S101', '2026-05-01', '2026-05-15')
        issue_book(self.conn, 1, 'S101', '2026-05-01', '2026-05-15')

        # Third attempt should fail
        success, msg = issue_book(self.conn, 1, 'S101', '2026-05-01', '2026-05-15')
        self.assertFalse(success)
        self.assertIn("No copies", msg)

    def test_issue_book_fails_for_nonexistent_student(self):
        success, msg = issue_book(self.conn, 1, 'NONEXISTENT', '2026-05-01', '2026-05-15')
        self.assertFalse(success)
        self.assertIn("Selected student does not exist", msg)

    def test_return_book_increments_available_and_sets_status(self):
        issue_book(self.conn, 1, 'S101', '2026-05-01', '2026-05-15')
        tx = self.conn.execute("SELECT id FROM transactions WHERE book_id = 1").fetchone()

        success, msg = return_book(self.conn, tx['id'], '2026-05-10')
        self.assertTrue(success)

        book = self.conn.execute("SELECT available FROM books WHERE id = 1").fetchone()
        self.assertEqual(book['available'], 2)

        tx_updated = self.conn.execute("SELECT status, return_date FROM transactions WHERE id = ?", (tx['id'],)).fetchone()
        self.assertEqual(tx_updated['status'], 'RETURNED')
        self.assertEqual(tx_updated['return_date'], '2026-05-10')

    def test_prevent_double_return(self):
        issue_book(self.conn, 1, 'S101', '2026-05-01', '2026-05-15')
        tx = self.conn.execute("SELECT id FROM transactions WHERE book_id = 1").fetchone()

        return_book(self.conn, tx['id'], '2026-05-10')
        # Attempt second return
        success, msg = return_book(self.conn, tx['id'], '2026-05-11')
        self.assertFalse(success)
        self.assertIn("already been returned", msg)

    def test_cannot_delete_book_with_active_loans(self):
        issue_book(self.conn, 1, 'S101', '2026-05-01', '2026-05-15')
        can_del, reason = can_delete_book(self.conn, 1)
        self.assertFalse(can_del)
        self.assertIn("currently issued", reason)

    def test_can_delete_book_after_return(self):
        issue_book(self.conn, 1, 'S101', '2026-05-01', '2026-05-15')
        tx = self.conn.execute("SELECT id FROM transactions WHERE book_id = 1").fetchone()
        return_book(self.conn, tx['id'], '2026-05-10')

        can_del, reason = can_delete_book(self.conn, 1)
        self.assertTrue(can_del)

    def test_cannot_delete_student_with_active_loans(self):
        issue_book(self.conn, 1, 'S101', '2026-05-01', '2026-05-15')
        can_del, reason = can_delete_student(self.conn, 'S101')
        self.assertFalse(can_del)
        self.assertIn("issued book", reason)


if __name__ == "__main__":
    unittest.main()

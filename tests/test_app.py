import unittest
import tempfile
import os
import sqlite3
from app import app
import database


class FlaskAppIntegrationTests(unittest.TestCase):
    def setUp(self):
        # Create a temporary SQLite database for test isolation
        self.db_fd, self.temp_db_path = tempfile.mkstemp(suffix=".db")
        self.orig_db_path = database.DATABASE
        database.DATABASE = self.temp_db_path

        app.config["TESTING"] = True
        app.config["SECRET_KEY"] = "test-secret"
        self.client = app.test_client()

        with app.app_context():
            database.init_db()
            # Seed test records
            db = database.get_db()
            db.execute(
                "INSERT INTO books (title, author, isbn, quantity, available) VALUES (?, ?, ?, ?, ?)",
                ("Test-Driven Development", "Kent Beck", "978-0321146533", 3, 3)
            )
            db.execute(
                "INSERT INTO students (student_id, name, email, department) VALUES (?, ?, ?, ?)",
                ("STU001", "Jane Student", "jane@university.edu", "CSE")
            )
            db.commit()

    def tearDown(self):
        # Restore database configuration and remove temporary file
        database.DATABASE = self.orig_db_path
        os.close(self.db_fd)
        if os.path.exists(self.temp_db_path):
            os.remove(self.temp_db_path)

    def test_root_redirects_to_dashboard(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/dashboard", response.headers["Location"])

    def test_dashboard_renders_stats(self):
        response = self.client.get("/dashboard")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Operational Dashboard", response.data)
        self.assertIn(b"Total Book Copies", response.data)

    def test_books_catalogue_renders(self):
        response = self.client.get("/books")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Test-Driven Development", response.data)

    def test_add_book_post_success(self):
        response = self.client.post("/books/add", data={
            "title": "Refactoring",
            "author": "Martin Fowler",
            "isbn": "978-0201485677",
            "quantity": "2"
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Refactoring", response.data)

    def test_students_page_renders(self):
        response = self.client.get("/students")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Jane Student", response.data)
        self.assertIn(b"STU001", response.data)

    def test_add_student_post_success(self):
        response = self.client.post("/students/add", data={
            "student_id": "STU002",
            "name": "Alan Turing",
            "email": "alan@enigma.edu",
            "department": "Mathematics"
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Alan Turing", response.data)

    def test_duplicate_student_id_rejected(self):
        response = self.client.post("/students/add", data={
            "student_id": "STU001",
            "name": "Duplicate Student",
            "email": "dup@test.edu",
            "department": "CSE"
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"already exists", response.data)

    def test_issue_and_return_cycle(self):
        # 1. Issue book
        issue_resp = self.client.post("/issue", data={
            "book_id": "1",
            "student_id": "STU001",
            "issue_date": "2026-05-01",
            "due_date": "2026-05-15"
        }, follow_redirects=True)
        self.assertEqual(issue_resp.status_code, 200)

        # Verify inventory decreased
        with app.app_context():
            db = database.get_db()
            book = db.execute("SELECT available FROM books WHERE id = 1").fetchone()
            self.assertEqual(book["available"], 2)
            tx = db.execute("SELECT id FROM transactions WHERE book_id = 1").fetchone()
            self.assertIsNotNone(tx)
            tx_id = tx["id"]

        # 2. Return book
        return_resp = self.client.post(f"/return/{tx_id}", data={
            "return_date": "2026-05-10"
        }, follow_redirects=True)
        self.assertEqual(return_resp.status_code, 200)

        # Verify inventory restored
        with app.app_context():
            db = database.get_db()
            book = db.execute("SELECT available FROM books WHERE id = 1").fetchone()
            self.assertEqual(book["available"], 3)
            tx = db.execute("SELECT status FROM transactions WHERE id = ?", (tx_id,)).fetchone()
            self.assertEqual(tx["status"], "RETURNED")

    def test_health_check(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"status": "ok"})


if __name__ == "__main__":
    unittest.main()

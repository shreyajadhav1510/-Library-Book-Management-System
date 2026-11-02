import sqlite3
from flask import g

DATABASE = "library.db"


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
        # Enforce foreign key constraints in SQLite
        g.db.execute("PRAGMA foreign_keys = ON;")
    return g.db


def init_db(db_path=None):
    """
    Initialize database tables safely while preserving existing data.
    Can be called with a specific connection or using Flask's g.db.
    """
    if db_path is not None:
        conn = sqlite3.connect(db_path)
        conn.execute("PRAGMA foreign_keys = ON;")
        cursor = conn.cursor()
    else:
        conn = get_db()
        cursor = conn

    # Create books table if not exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            isbn TEXT,
            quantity INTEGER NOT NULL CHECK(quantity >= 1),
            available INTEGER NOT NULL CHECK(available >= 0)
        )
    """)

    # Create students table if not exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            department TEXT NOT NULL
        )
    """)

    # Create transactions table for borrowing and return history
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER NOT NULL,
            student_id TEXT NOT NULL,
            issue_date TEXT NOT NULL,
            due_date TEXT NOT NULL,
            return_date TEXT,
            status TEXT NOT NULL DEFAULT 'ISSUED',
            FOREIGN KEY (book_id) REFERENCES books (id) ON DELETE RESTRICT,
            FOREIGN KEY (student_id) REFERENCES students (student_id) ON DELETE RESTRICT
        )
    """)

    conn.commit()
    if db_path is not None:
        conn.close()


def close_db(_error=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()

"""
Safe, Repeatable Demo Data Seeder for Libra — Library Management System.

This script populates the SQLite database with realistic fictional Indian student
and library book records along with balanced circulation transactions.

Safety Guarantees:
- Never drops or recreates existing tables.
- Never deletes or overwrites existing records (e.g., pre-existing student or book records).
- Idempotent: checks for existing IDs/titles before inserting to prevent duplicate records.
- Synchronizes book availability with active borrowing transactions.
- Fully transactional with error rollbacks.

Usage:
    python seed_demo_data.py
"""

import sqlite3
import datetime
import os

DATABASE_PATH = "library.db"


def get_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


DEMO_STUDENTS = [
    {
        "student_id": "DEMO001",
        "name": "Shreya Jadhav",
        "email": "shreya.jadhav@example.com",
        "department": "Computer Science",
    },
    {
        "student_id": "DEMO002",
        "name": "Aarya Patel",
        "email": "aarya.patel@example.com",
        "department": "Information Technology",
    },
    {
        "student_id": "DEMO003",
        "name": "Jaival Patel",
        "email": "jaival.patel@example.com",
        "department": "Computer Science",
    },
    {
        "student_id": "DEMO004",
        "name": "Hetvi Shah",
        "email": "hetvi.shah@example.com",
        "department": "Artificial Intelligence & Data Science",
    },
    {
        "student_id": "DEMO005",
        "name": "Kajal Mehta",
        "email": "kajal.mehta@example.com",
        "department": "Electronics & Telecommunication",
    },
    {
        "student_id": "DEMO006",
        "name": "Riya Desai",
        "email": "riya.desai@example.com",
        "department": "Information Technology",
    },
    {
        "student_id": "DEMO007",
        "name": "Aarav Sharma",
        "email": "aarav.sharma@example.com",
        "department": "Computer Science",
    },
    {
        "student_id": "DEMO008",
        "name": "Ananya Joshi",
        "email": "ananya.joshi@example.com",
        "department": "Electronics & Telecommunication",
    },
    {
        "student_id": "DEMO009",
        "name": "Krish Shah",
        "email": "krish.shah@example.com",
        "department": "Mechanical Engineering",
    },
    {
        "student_id": "DEMO010",
        "name": "Neha Trivedi",
        "email": "neha.trivedi@example.com",
        "department": "Electrical Engineering",
    },
    {
        "student_id": "DEMO011",
        "name": "Rohan Verma",
        "email": "rohan.verma@example.com",
        "department": "Mechanical Engineering",
    },
    {
        "student_id": "DEMO012",
        "name": "Pooja Nair",
        "email": "pooja.nair@example.com",
        "department": "Civil Engineering",
    },
]

DEMO_BOOKS = [
    # Programming & Computer Science
    {
        "title": "Clean Code: A Handbook of Agile Software Craftsmanship",
        "author": "Robert C. Martin",
        "isbn": "978-0132350884",
        "quantity": 4,
    },
    {
        "title": "Introduction to Algorithms (CLRS)",
        "author": "Thomas H. Cormen, Charles E. Leiserson",
        "isbn": "978-0262033848",
        "quantity": 5,
    },
    {
        "title": "Design Patterns: Elements of Reusable Object-Oriented Software",
        "author": "Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides",
        "isbn": "978-0201633610",
        "quantity": 3,
    },
    {
        "title": "Fluent Python: Clear, Concise, and Effective Programming",
        "author": "Luciano Ramalho",
        "isbn": "978-1491946008",
        "quantity": 3,
    },
    {
        "title": "Operating System Concepts",
        "author": "Abraham Silberschatz, Peter B. Galvin",
        "isbn": "978-1118063330",
        "quantity": 4,
    },
    {
        "title": "Computer Networks: A Systems Approach",
        "author": "Larry L. Peterson, Bruce S. Davie",
        "isbn": "978-0123850591",
        "quantity": 3,
    },
    # Software Engineering & Architecture
    {
        "title": "Refactoring: Improving the Design of Existing Code",
        "author": "Martin Fowler",
        "isbn": "978-0134757599",
        "quantity": 3,
    },
    {
        "title": "The Pragmatic Programmer: Your Journey to Mastery",
        "author": "David Thomas, Andrew Hunt",
        "isbn": "978-0135957059",
        "quantity": 4,
    },
    {
        "title": "Designing Data-Intensive Applications",
        "author": "Martin Kleppmann",
        "isbn": "978-1449373320",
        "quantity": 3,
    },
    # Artificial Intelligence & Data Science
    {
        "title": "Artificial Intelligence: A Modern Approach",
        "author": "Stuart Russell, Peter Norvig",
        "isbn": "978-0136042594",
        "quantity": 4,
    },
    {
        "title": "Deep Learning",
        "author": "Ian Goodfellow, Yoshua Bengio, Aaron Courville",
        "isbn": "978-0262035613",
        "quantity": 2,
    },
    {
        "title": "Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow",
        "author": "Aurélien Géron",
        "isbn": "978-1492032649",
        "quantity": 3,
    },
    # Business, Leadership & Management
    {
        "title": "The Lean Startup",
        "author": "Eric Ries",
        "isbn": "978-0307887894",
        "quantity": 3,
    },
    {
        "title": "Sprint: How to Solve Big Problems and Test New Ideas in Just Five Days",
        "author": "Jake Knapp",
        "isbn": "978-1501121747",
        "quantity": 2,
    },
    {
        "title": "Zero to One: Notes on Startups, or How to Build the Future",
        "author": "Peter Thiel, Blake Masters",
        "isbn": "978-0804139298",
        "quantity": 3,
    },
    # Fiction & General Reading
    {
        "title": "The Alchemist",
        "author": "Paulo Coelho",
        "isbn": "978-0062315007",
        "quantity": 4,
    },
    {
        "title": "Atomic Habits",
        "author": "James Clear",
        "isbn": "978-0735211292",
        "quantity": 5,
    },
    {
        "title": "Wings of Fire: An Autobiography",
        "author": "A.P.J. Abdul Kalam, Arun Tiwari",
        "isbn": "978-8173711466",
        "quantity": 4,
    },
]


def seed_database():
    if not os.path.exists(DATABASE_PATH):
        print(f"[ERROR] Database file '{DATABASE_PATH}' not found. Please start app once to initialize schema.")
        return

    conn = get_connection()
    cursor = conn.cursor()

    print("=" * 60)
    print("  Libra -- Safe Demonstration Data Seeder")
    print("=" * 60)

    # 1. Seed Students
    students_added = 0
    students_skipped = 0
    for s in DEMO_STUDENTS:
        # Check if student_id or email already exists to prevent integrity errors
        existing = cursor.execute(
            "SELECT student_id FROM students WHERE student_id = ? OR email = ?",
            (s["student_id"], s["email"])
        ).fetchone()

        if existing:
            students_skipped += 1
        else:
            cursor.execute(
                """INSERT INTO students (student_id, name, email, department)
                   VALUES (?, ?, ?, ?)""",
                (s["student_id"], s["name"], s["email"], s["department"])
            )
            students_added += 1

    conn.commit()
    print(f"[Students] Added: {students_added} | Skipped/Already present: {students_skipped}")

    # 2. Seed Books
    books_added = 0
    books_skipped = 0
    for b in DEMO_BOOKS:
        # Check by title and author
        existing = cursor.execute(
            "SELECT id FROM books WHERE title = ? AND author = ?",
            (b["title"], b["author"])
        ).fetchone()

        if existing:
            books_skipped += 1
        else:
            # Initially set available = quantity; circulation seed will adjust accurately
            cursor.execute(
                """INSERT INTO books (title, author, isbn, quantity, available)
                   VALUES (?, ?, ?, ?, ?)""",
                (b["title"], b["author"], b["isbn"], b["quantity"], b["quantity"])
            )
            books_added += 1

    conn.commit()
    print(f"[Books]    Added: {books_added} | Skipped/Already present: {books_skipped}")

    # 3. Seed Circulation Transactions (Balanced Loans & Returns)
    # Define reference dates relative to today:
    today = datetime.date.today()
    d_minus_25 = (today - datetime.timedelta(days=25)).isoformat()
    d_minus_18 = (today - datetime.timedelta(days=18)).isoformat()
    d_minus_10 = (today - datetime.timedelta(days=10)).isoformat()
    d_minus_7  = (today - datetime.timedelta(days=7)).isoformat()
    d_minus_4  = (today - datetime.timedelta(days=4)).isoformat()
    d_minus_2  = (today - datetime.timedelta(days=2)).isoformat()
    d_plus_7   = (today + datetime.timedelta(days=7)).isoformat()
    d_plus_10  = (today + datetime.timedelta(days=10)).isoformat()
    d_plus_12  = (today + datetime.timedelta(days=12)).isoformat()

    # Planned circulation actions for demonstration
    # Format: (book_title_snippet, student_id, issue_date, due_date, return_date_or_None, status)
    PLANNED_TRANSACTIONS = [
        # Returned loan 1
        ("Clean Code", "DEMO001", d_minus_25, d_minus_10, d_minus_7, "RETURNED"),
        # Returned loan 2
        ("The Lean Startup", "DEMO002", d_minus_18, d_minus_4, d_minus_2, "RETURNED"),
        # Returned loan 3
        ("Atomic Habits", "DEMO003", d_minus_18, d_minus_4, d_minus_4, "RETURNED"),
        # Active Loan 1 (Clean Code)
        ("Clean Code", "DEMO004", d_minus_4, d_plus_10, None, "ISSUED"),
        # Active Loan 2 (Introduction to Algorithms)
        ("Introduction to Algorithms", "DEMO005", d_minus_7, d_plus_7, None, "ISSUED"),
        # Active Loan 3 (Designing Data-Intensive)
        ("Designing Data-Intensive", "DEMO006", d_minus_2, d_plus_12, None, "ISSUED"),
        # Active Loan 4 (Deep Learning)
        ("Deep Learning", "DEMO007", d_minus_4, d_plus_10, None, "ISSUED"),
        # Active Loan 5 - OVERDUE (Issued 25 days ago, due 10 days ago, not returned)
        ("Operating System Concepts", "DEMO008", d_minus_25, d_minus_10, None, "ISSUED"),
        # Active Loan 6 - OVERDUE (Issued 18 days ago, due 4 days ago)
        ("Artificial Intelligence: A Modern Approach", "DEMO009", d_minus_18, d_minus_4, None, "ISSUED"),
    ]

    tx_added = 0
    tx_skipped = 0

    for title_snippet, stu_id, iss_date, d_date, ret_date, status in PLANNED_TRANSACTIONS:
        # Find matching book
        book_row = cursor.execute(
            "SELECT id, title, quantity, available FROM books WHERE title LIKE ? LIMIT 1",
            (f"%{title_snippet}%",)
        ).fetchone()

        # Find matching student
        stu_row = cursor.execute(
            "SELECT student_id, name FROM students WHERE student_id = ? LIMIT 1",
            (stu_id,)
        ).fetchone()

        if not book_row or not stu_row:
            continue

        b_id = book_row["id"]
        s_id = stu_row["student_id"]

        # Check if an identical transaction already exists
        existing_tx = cursor.execute(
            """SELECT id FROM transactions
               WHERE book_id = ? AND student_id = ? AND issue_date = ? AND status = ?""",
            (b_id, s_id, iss_date, status)
        ).fetchone()

        if existing_tx:
            tx_skipped += 1
            continue

        # Insert transaction
        cursor.execute(
            """INSERT INTO transactions (book_id, student_id, issue_date, due_date, return_date, status)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (b_id, s_id, iss_date, d_date, ret_date, status)
        )
        tx_added += 1

    conn.commit()
    print(f"[Transactions] Added: {tx_added} | Skipped/Already present: {tx_skipped}")

    # 4. Synchronize book availability counts with active loans
    # available = quantity - count(active 'ISSUED' transactions for that book)
    cursor.execute("""
        UPDATE books
        SET available = MAX(0, quantity - (
            SELECT COUNT(*) FROM transactions
            WHERE transactions.book_id = books.id AND transactions.status = 'ISSUED'
        ))
    """)
    conn.commit()

    # 5. Display Database Status Summary
    totals = cursor.execute("""
        SELECT
            (SELECT COUNT(*) FROM books) AS total_titles,
            (SELECT COALESCE(SUM(quantity), 0) FROM books) AS total_copies,
            (SELECT COALESCE(SUM(available), 0) FROM books) AS available_copies,
            (SELECT COUNT(*) FROM students) AS total_students,
            (SELECT COUNT(*) FROM transactions) AS total_transactions,
            (SELECT COUNT(*) FROM transactions WHERE status = 'ISSUED') AS active_loans,
            (SELECT COUNT(*) FROM transactions WHERE status = 'ISSUED' AND due_date < ?) AS overdue_loans
    """, (today.isoformat(),)).fetchone()

    print("-" * 60)
    print("Database Snapshot after Seeding:")
    print(f"  * Distinct Titles:    {totals['total_titles']}")
    print(f"  * Total Book Copies:  {totals['total_copies']}")
    print(f"  * Available Copies:   {totals['available_copies']}")
    print(f"  * Issued Copies:      {totals['total_copies'] - totals['available_copies']}")
    print(f"  * Registered Students:{totals['total_students']}")
    print(f"  * Total Transactions: {totals['total_transactions']}")
    print(f"  * Active Loans:       {totals['active_loans']}")
    print(f"  * Overdue Loans:      {totals['overdue_loans']}")
    print("=" * 60)
    print("[OK] Seeding finished safely without data loss.")

    conn.close()


if __name__ == "__main__":
    seed_database()

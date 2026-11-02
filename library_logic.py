import re
import datetime


def validate_book(title, author, quantity_text):
    """Return an error message when book input is invalid; otherwise None."""
    if not title or not title.strip():
        return "Please enter a book title."
    if not author or not author.strip():
        return "Please enter the author's name."
    try:
        quantity = int(quantity_text)
    except (TypeError, ValueError):
        return "Quantity must be a whole number."
    if quantity < 1:
        return "Quantity must be at least 1."
    return None


def search_books(books, query):
    """Case-insensitive search across book title and author."""
    if not query or not query.strip():
        return list(books)
    term = query.strip().casefold()
    return [
        book for book in books
        if term in book["title"].casefold() or term in book["author"].casefold()
    ]


def validate_student(student_id, name, email, department):
    """Return an error message when student input is invalid; otherwise None."""
    if not student_id or not student_id.strip():
        return "Student ID is required."
    if not name or not name.strip():
        return "Student name is required."
    if not email or not email.strip():
        return "Student email is required."
    if not department or not department.strip():
        return "Department is required."

    email_regex = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    if not re.match(email_regex, email.strip()):
        return "Please enter a valid email address."

    return None


def calculate_overdue(due_date_str, return_date_str=None, current_date=None):
    """
    Determine if a transaction is overdue.
    If already returned, overdue is based on whether return_date > due_date.
    If not yet returned, overdue is based on whether current_date > due_date.
    """
    try:
        due_date = datetime.date.fromisoformat(due_date_str)
    except (ValueError, TypeError):
        return False

    if return_date_str:
        try:
            return_date = datetime.date.fromisoformat(return_date_str)
            return return_date > due_date
        except (ValueError, TypeError):
            return False

    ref_date = current_date if current_date else datetime.date.today()
    return ref_date > due_date


def issue_book(db, book_id, student_id, issue_date, due_date):
    """
    Issue a book to a student atomically.
    Returns (success: bool, message: str).
    """
    try:
        # Check student exists
        student = db.execute(
            "SELECT student_id, name FROM students WHERE student_id = ?",
            (student_id,)
        ).fetchone()
        if not student:
            return False, "Selected student does not exist."

        # Check book exists and has available copies
        book = db.execute(
            "SELECT id, title, available FROM books WHERE id = ?",
            (book_id,)
        ).fetchone()
        if not book:
            return False, "Selected book does not exist."

        if book["available"] <= 0:
            return False, f"No copies of '{book['title']}' are currently available."

        # Decrease available count
        db.execute(
            "UPDATE books SET available = available - 1 WHERE id = ?",
            (book_id,)
        )

        # Record transaction
        db.execute(
            """INSERT INTO transactions
               (book_id, student_id, issue_date, due_date, status)
               VALUES (?, ?, ?, ?, 'ISSUED')""",
            (book_id, student_id, issue_date, due_date)
        )
        db.commit()
        return True, f"'{book['title']}' successfully issued to {student['name']}."
    except Exception as e:
        db.rollback()
        return False, f"Failed to issue book: {str(e)}"


def return_book(db, transaction_id, return_date):
    """
    Return a borrowed book atomically.
    Returns (success: bool, message: str).
    """
    try:
        tx = db.execute(
            """SELECT t.id, t.book_id, t.status, b.title, b.available, b.quantity
               FROM transactions t
               JOIN books b ON t.book_id = b.id
               WHERE t.id = ?""",
            (transaction_id,)
        ).fetchone()

        if not tx:
            return False, "Transaction record not found."

        if tx["status"] == "RETURNED":
            return False, "This book has already been returned."

        # Increase available count (ensuring it doesn't exceed total quantity)
        new_available = min(tx["quantity"], tx["available"] + 1)
        db.execute(
            "UPDATE books SET available = ? WHERE id = ?",
            (new_available, tx["book_id"])
        )

        # Update transaction status
        db.execute(
            """UPDATE transactions
               SET return_date = ?, status = 'RETURNED'
               WHERE id = ?""",
            (return_date, transaction_id)
        )
        db.commit()
        return True, f"'{tx['title']}' was successfully returned."
    except Exception as e:
        db.rollback()
        return False, f"Failed to return book: {str(e)}"


def can_delete_book(db, book_id):
    """
    Returns (can_delete: bool, reason: str).
    Prevents deletion if there are active loans.
    """
    active_loans = db.execute(
        "SELECT COUNT(*) FROM transactions WHERE book_id = ? AND status = 'ISSUED'",
        (book_id,)
    ).fetchone()[0]

    if active_loans > 0:
        return False, f"Cannot delete book: There are {active_loans} copy/copies currently issued."
    return True, ""


def can_delete_student(db, student_id):
    """
    Returns (can_delete: bool, reason: str).
    Prevents deletion if student has active book loans.
    """
    active_loans = db.execute(
        "SELECT COUNT(*) FROM transactions WHERE student_id = ? AND status = 'ISSUED'",
        (student_id,)
    ).fetchone()[0]

    if active_loans > 0:
        return False, f"Cannot delete student: Student currently has {active_loans} issued book(s)."
    return True, ""

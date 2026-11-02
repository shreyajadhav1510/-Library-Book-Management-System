import datetime
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash
from database import init_db, get_db, close_db
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

app = Flask(__name__)
app.secret_key = "library-project-secret-key"
app.teardown_appcontext(close_db)


# -------------------------------------------------------------
# Root & Dashboard Routes
# -------------------------------------------------------------
@app.route("/")
def root():
    return redirect(url_for("dashboard"))


@app.route("/index")
def index():
    return redirect(url_for("dashboard"))


@app.route("/dashboard")
def dashboard():
    db = get_db()

    # Calculate real summary counts from database
    book_totals = db.execute(
        "SELECT COALESCE(SUM(quantity), 0) AS total_qty, COALESCE(SUM(available), 0) AS total_avail FROM books"
    ).fetchone()
    total_books = book_totals["total_qty"]
    total_available = book_totals["total_avail"]
    total_issued = max(0, total_books - total_available)

    total_students = db.execute("SELECT COUNT(*) FROM students").fetchone()[0]

    # Fetch 5 most recent circulation transactions
    raw_txs = db.execute(
        """SELECT t.id, t.book_id, t.student_id, t.issue_date, t.due_date, t.return_date, t.status,
                  b.title AS book_title, s.name AS student_name
           FROM transactions t
           LEFT JOIN books b ON t.book_id = b.id
           LEFT JOIN students s ON t.student_id = s.student_id
           ORDER BY t.id DESC LIMIT 5"""
    ).fetchall()

    recent_transactions = []
    today_str = datetime.date.today().isoformat()
    for tx in raw_txs:
        tx_dict = dict(tx)
        tx_dict["is_overdue"] = calculate_overdue(tx["due_date"], tx["return_date"])
        recent_transactions.append(tx_dict)

    overdue_loans = db.execute(
        "SELECT COUNT(*) FROM transactions WHERE status = 'ISSUED' AND due_date < ?",
        (today_str,)
    ).fetchone()[0]

    return render_template(
        "dashboard.html",
        active_page="dashboard",
        total_books=total_books,
        total_available=total_available,
        total_issued=total_issued,
        total_students=total_students,
        overdue_loans=overdue_loans,
        recent_transactions=recent_transactions,
    )


# -------------------------------------------------------------
# Books Management Routes
# -------------------------------------------------------------
@app.route("/books")
def books_page():
    db = get_db()
    query = request.args.get("q", "").strip()

    if query:
        # Use case-insensitive search across title and author
        books = db.execute(
            """SELECT * FROM books
               WHERE title LIKE ? OR author LIKE ?
               ORDER BY id DESC""",
            (f"%{query}%", f"%{query}%")
        ).fetchall()
    else:
        books = db.execute("SELECT * FROM books ORDER BY id DESC").fetchall()

    return render_template(
        "books.html",
        active_page="books",
        books=books,
        query=query
    )


@app.route("/books/add", methods=["POST"])
def add_book():
    title = request.form.get("title", "").strip()
    author = request.form.get("author", "").strip()
    isbn = request.form.get("isbn", "").strip()
    quantity_text = request.form.get("quantity", "1").strip()

    error = validate_book(title, author, quantity_text)
    if error:
        flash(error, "error")
        # Render books page with existing books and error flash
        db = get_db()
        books = db.execute("SELECT * FROM books ORDER BY id DESC").fetchall()
        return render_template("books.html", active_page="books", books=books, query="")

    quantity = int(quantity_text)
    db = get_db()
    try:
        db.execute(
            """INSERT INTO books (title, author, isbn, quantity, available)
               VALUES (?, ?, ?, ?, ?)""",
            (title, author, isbn, quantity, quantity)
        )
        db.commit()
        flash("added successfully", "success")
        # Redirect to books page to display flash message using PRG pattern
        return redirect(url_for('books_page'))
    except Exception as e:
        db.rollback()
        flash("Error adding book.", "error")
        # Render books page with current books and error flash
        books = db.execute("SELECT * FROM books ORDER BY id DESC").fetchall()
        return render_template("books.html", active_page="books", books=books, query="")


@app.route("/books/<int:book_id>/edit", methods=["GET"])
def edit_book_page(book_id):
    db = get_db()
    book = db.execute("SELECT * FROM books WHERE id = ?", (book_id,)).fetchone()
    if not book:
        flash("Book not found.", "error")
        return redirect(url_for("books_page"))
    return render_template("edit_book.html", active_page="books", book=book)


@app.route("/books/<int:book_id>/edit", methods=["POST"])
def edit_book_action(book_id):
    db = get_db()
    book = db.execute("SELECT * FROM books WHERE id = ?", (book_id,)).fetchone()
    if not book:
        flash("Book not found.", "error")
        return redirect(url_for("books_page"))

    title = request.form.get("title", "").strip()
    author = request.form.get("author", "").strip()
    isbn = request.form.get("isbn", "").strip()
    quantity_text = request.form.get("quantity", "").strip()

    error = validate_book(title, author, quantity_text)
    if error:
        flash(error, "error")
        return redirect(url_for("edit_book_page", book_id=book_id))

    new_quantity = int(quantity_text)
    currently_issued = book["quantity"] - book["available"]

    if new_quantity < currently_issued:
        flash(
            f"Cannot reduce total quantity below currently issued copies ({currently_issued}).",
            "error"
        )
        return redirect(url_for("edit_book_page", book_id=book_id))

    new_available = new_quantity - currently_issued

    try:
        db.execute(
            """UPDATE books
               SET title = ?, author = ?, isbn = ?, quantity = ?, available = ?
               WHERE id = ?""",
            (title, author, isbn, new_quantity, new_available, book_id)
        )
        db.commit()
        flash(f"Book '{title}' updated successfully.", "success")
    except Exception as e:
        db.rollback()
        flash(f"Error updating book: {str(e)}", "error")

    return redirect(url_for("books_page"))


@app.route("/books/<int:book_id>/delete", methods=["POST"])
def delete_book(book_id):
    db = get_db()

    can_del, reason = can_delete_book(db, book_id)
    if not can_del:
        flash(reason, "error")
        return redirect(url_for("books_page"))

    try:
        db.execute("DELETE FROM books WHERE id = ?", (book_id,))
        db.commit()
        flash("Book deleted from catalogue.", "success")
    except sqlite3.IntegrityError:
        db.rollback()
        flash("Cannot delete book with existing historical borrowing records.", "error")
    except Exception as e:
        db.rollback()
        flash(f"Error deleting book: {str(e)}", "error")

    return redirect(url_for("books_page"))


# -------------------------------------------------------------
# Student Management Routes
# -------------------------------------------------------------
@app.route("/students")
def students_page():
    db = get_db()
    query = request.args.get("q", "").strip()

    if query:
        students = db.execute(
            """SELECT s.*, 
                      (SELECT COUNT(*) FROM transactions t WHERE t.student_id = s.student_id AND t.status = 'ISSUED') AS active_loans
               FROM students s
               WHERE s.student_id LIKE ? OR s.name LIKE ? OR s.email LIKE ?
               ORDER BY s.id DESC""",
            (f"%{query}%", f"%{query}%", f"%{query}%")
        ).fetchall()
    else:
        students = db.execute(
            """SELECT s.*,
                      (SELECT COUNT(*) FROM transactions t WHERE t.student_id = s.student_id AND t.status = 'ISSUED') AS active_loans
               FROM students s
               ORDER BY s.id DESC"""
        ).fetchall()

    return render_template(
        "students.html",
        active_page="students",
        students=students,
        query=query
    )


@app.route("/students/add", methods=["POST"])
def add_student():
    student_id = request.form.get("student_id", "").strip()
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    department = request.form.get("department", "").strip()

    error = validate_student(student_id, name, email, department)
    if error:
        flash(error, "error")
        return redirect(url_for("students_page"))

    db = get_db()
    try:
        db.execute(
            """INSERT INTO students (student_id, name, email, department)
               VALUES (?, ?, ?, ?)""",
            (student_id, name, email, department)
        )
        db.commit()
        flash(f"Student '{name}' registered successfully.", "success")
    except sqlite3.IntegrityError:
        db.rollback()
        flash("Student ID or Email already exists in the system.", "error")
    except Exception as e:
        db.rollback()
        flash(f"Error registering student: {str(e)}", "error")

    return redirect(url_for("students_page"))


@app.route("/students/<student_id>/edit", methods=["GET"])
def edit_student_page(student_id):
    db = get_db()
    student = db.execute(
        "SELECT * FROM students WHERE student_id = ?",
        (student_id,)
    ).fetchone()

    if not student:
        flash("Student record not found.", "error")
        return redirect(url_for("students_page"))

    return render_template("edit_student.html", active_page="students", student=student)


@app.route("/students/<student_id>/edit", methods=["POST"])
def edit_student_action(student_id):
    db = get_db()
    student = db.execute(
        "SELECT * FROM students WHERE student_id = ?",
        (student_id,)
    ).fetchone()

    if not student:
        flash("Student record not found.", "error")
        return redirect(url_for("students_page"))

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    department = request.form.get("department", "").strip()

    error = validate_student(student_id, name, email, department)
    if error:
        flash(error, "error")
        return redirect(url_for("edit_student_page", student_id=student_id))

    try:
        db.execute(
            """UPDATE students
               SET name = ?, email = ?, department = ?
               WHERE student_id = ?""",
            (name, email, department, student_id)
        )
        db.commit()
        flash(f"Student '{name}' updated successfully.", "success")
    except sqlite3.IntegrityError:
        db.rollback()
        flash("Another student with that email address already exists.", "error")
    except Exception as e:
        db.rollback()
        flash(f"Error updating student: {str(e)}", "error")

    return redirect(url_for("students_page"))


@app.route("/students/<student_id>/delete", methods=["POST"])
def delete_student(student_id):
    db = get_db()

    can_del, reason = can_delete_student(db, student_id)
    if not can_del:
        flash(reason, "error")
        return redirect(url_for("students_page"))

    try:
        db.execute("DELETE FROM students WHERE student_id = ?", (student_id,))
        db.commit()
        flash("Student record deleted.", "success")
    except sqlite3.IntegrityError:
        db.rollback()
        flash("Cannot delete student with historical borrowing transactions.", "error")
    except Exception as e:
        db.rollback()
        flash(f"Error deleting student: {str(e)}", "error")

    return redirect(url_for("students_page"))


# -------------------------------------------------------------
# Issue & Return Circulation Routes
# -------------------------------------------------------------
@app.route("/issue-return")
def issue_return_page():
    db = get_db()
    students = db.execute("SELECT * FROM students ORDER BY name ASC").fetchall()
    available_books = db.execute(
        "SELECT * FROM books WHERE available > 0 ORDER BY title ASC"
    ).fetchall()

    raw_loans = db.execute(
        """SELECT t.id, t.book_id, t.student_id, t.issue_date, t.due_date, t.return_date, t.status,
                  b.title AS book_title, s.name AS student_name, s.department
           FROM transactions t
           JOIN books b ON t.book_id = b.id
           JOIN students s ON t.student_id = s.student_id
           WHERE t.status = 'ISSUED'
           ORDER BY t.due_date ASC"""
    ).fetchall()

    today = datetime.date.today()
    default_issue_date = today.isoformat()
    default_due_date = (today + datetime.timedelta(days=14)).isoformat()

    active_loans = []
    for loan in raw_loans:
        loan_dict = dict(loan)
        loan_dict["is_overdue"] = calculate_overdue(loan["due_date"])
        active_loans.append(loan_dict)

    return render_template(
        "issue_return.html",
        active_page="issue_return",
        students=students,
        available_books=available_books,
        active_loans=active_loans,
        default_issue_date=default_issue_date,
        default_due_date=default_due_date,
    )


@app.route("/issue", methods=["POST"])
def issue_book_action():
    book_id_text = request.form.get("book_id", "").strip()
    student_id = request.form.get("student_id", "").strip()
    issue_date = request.form.get("issue_date", "").strip()
    due_date = request.form.get("due_date", "").strip()

    if not book_id_text or not student_id or not issue_date or not due_date:
        flash("All issue fields are required.", "error")
        return redirect(url_for("issue_return_page"))

    try:
        book_id = int(book_id_text)
    except ValueError:
        flash("Invalid book selection.", "error")
        return redirect(url_for("issue_return_page"))

    db = get_db()
    success, message = issue_book(db, book_id, student_id, issue_date, due_date)
    flash(message, "success" if success else "error")
    return redirect(url_for("issue_return_page"))


@app.route("/return/<int:transaction_id>", methods=["POST"])
def return_book_action(transaction_id):
    return_date = request.form.get("return_date", "").strip()
    if not return_date:
        return_date = datetime.date.today().isoformat()

    db = get_db()
    success, message = return_book(db, transaction_id, return_date)
    flash(message, "success" if success else "error")
    return redirect(url_for("issue_return_page"))


# -------------------------------------------------------------
# Transactions History Route
# -------------------------------------------------------------
@app.route("/transactions")
def transactions_page():
    db = get_db()
    query = request.args.get("q", "").strip()
    status_filter = request.args.get("status", "").strip().upper()

    sql = """SELECT t.id, t.book_id, t.student_id, t.issue_date, t.due_date, t.return_date, t.status,
                    b.title AS book_title, s.name AS student_name, s.department
             FROM transactions t
             LEFT JOIN books b ON t.book_id = b.id
             LEFT JOIN students s ON t.student_id = s.student_id
             WHERE 1=1"""
    params = []

    if query:
        sql += " AND (b.title LIKE ? OR s.name LIKE ? OR s.student_id LIKE ?)"
        term = f"%{query}%"
        params.extend([term, term, term])

    if status_filter in ["ISSUED", "RETURNED"]:
        sql += " AND t.status = ?"
        params.append(status_filter)

    sql += " ORDER BY t.id DESC"

    raw_txs = db.execute(sql, params).fetchall()

    transactions = []
    for tx in raw_txs:
        tx_dict = dict(tx)
        is_overdue = calculate_overdue(tx["due_date"], tx["return_date"])
        tx_dict["is_overdue"] = is_overdue

        # If filtering specifically for OVERDUE
        if status_filter == "OVERDUE":
            if is_overdue and tx["status"] == "ISSUED":
                transactions.append(tx_dict)
        else:
            transactions.append(tx_dict)

    return render_template(
        "transactions.html",
        active_page="transactions",
        transactions=transactions,
        query=query,
        status_filter=status_filter
    )


# -------------------------------------------------------------
# Health Check Route
# -------------------------------------------------------------
@app.route("/health")
def health():
    return {"status": "ok"}, 200


with app.app_context():
    init_db()


if __name__ == "__main__":
    app.run(debug=True)

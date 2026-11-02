
import sqlite3
import os

print("Current folder:", os.getcwd())

if os.path.exists("library.db"):
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table'"
    )
    print("Tables:", cursor.fetchall())

    cursor.execute("SELECT * FROM books")
    for book in cursor.fetchall():
        print(book)

    conn.close()
else:
    print("Database file not found.")

import sqlite3
import os

DB_NAME = "library.db"


def init_db():
    """Initializes the database using the schema.sql file."""
    if not os.path.exists("schema.sql"):
        print("Error: schema.sql file not found!")
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    with open("schema.sql", "r") as f:
        sql_script = f.read()

    cursor.executescript(sql_script)
    conn.commit()
    conn.close()
    print("Database initialized successfully with sample data.")


def get_connection():
    """Returns a connection to the SQLite database with foreign keys enabled."""
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


# ==========================================
# BOOK CRUD OPERATIONS
# ==========================================

def add_book(title, author, isbn, copies):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO books (title, author, isbn, available_copies) VALUES (?, ?, ?, ?)",
            (title, author, isbn, copies)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        print("\n[Error] A book with this ISBN already exists.")
        return False
    finally:
        conn.close()


def list_books():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    conn.close()
    return books


def update_book(book_id, title, author, isbn, copies):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE books SET title=?, author=?, isbn=?, available_copies=? WHERE book_id=?",
        (title, author, isbn, copies, book_id)
    )
    conn.commit()
    rows_affected = cursor.rowcount
    conn.close()
    return rows_affected > 0


def delete_book(book_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE book_id=?", (book_id,))
    conn.commit()
    rows_affected = cursor.rowcount
    conn.close()
    return rows_affected > 0


# ==========================================
# MEMBER CRUD OPERATIONS
# ==========================================

def add_member(name, email):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO members (name, email) VALUES (?, ?)", (name, email))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        print("\n[Error] A member with this email already exists.")
        return False
    finally:
        conn.close()


def list_members():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM members")
    members = cursor.fetchall()
    conn.close()
    return members


# ==========================================
# LOAN OPERATIONS (TRANSACTIONS)
# ==========================================

def issue_loan(book_id, member_id):
    conn = get_connection()
    cursor = conn.cursor()

    # Check if book is available
    cursor.execute("SELECT available_copies FROM books WHERE book_id=?", (book_id,))
    result = cursor.fetchone()

    if not result or result[0] <= 0:
        print("\n[Error] Book is currently unavailable.")
        conn.close()
        return False

    try:
        # Issue loan and decrease available copies
        cursor.execute("INSERT INTO loans (book_id, member_id) VALUES (?, ?)", (book_id, member_id))
        cursor.execute("UPDATE books SET available_copies = available_copies - 1 WHERE book_id=?", (book_id,))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        print("\n[Error] Invalid Book ID or Member ID.")
        return False
    finally:
        conn.close()


def return_book(loan_id):
    conn = get_connection()
    cursor = conn.cursor()

    # Find the loan details
    cursor.execute("SELECT book_id, return_date FROM loans WHERE loan_id=?", (loan_id,))
    loan = cursor.fetchone()

    if not loan:
        print("\n[Error] Loan record not found.")
        conn.close()
        return False
    if loan[1] is not None:
        print("\n[Error] This book has already been returned.")
        conn.close()
        return False

    book_id = loan[0]
    # Mark as returned and increase available copies
    cursor.execute("UPDATE loans SET return_date = CURRENT_DATE WHERE loan_id=?", (loan_id,))
    cursor.execute("UPDATE books SET available_copies = available_copies + 1 WHERE book_id=?", (book_id,))
    conn.commit()
    conn.close()
    return True


def list_loans():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT l.loan_id, b.title, m.name, l.loan_date, l.return_date
                   FROM loans l
                            JOIN books b ON l.book_id = b.book_id
                            JOIN members m ON l.member_id = m.member_id
                   """)
    loans = cursor.fetchall()
    conn.close()
    return loans
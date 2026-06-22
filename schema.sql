-- Enable foreign key support in SQLite
PRAGMA foreign_keys = ON;

-- 1. Create Books Table
CREATE TABLE IF NOT EXISTS books (
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    isbn TEXT UNIQUE NOT NULL,
    available_copies INTEGER DEFAULT 1
);

-- 2. Create Members Table
CREATE TABLE IF NOT EXISTS members (
    member_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    join_date DATE DEFAULT CURRENT_DATE
);

-- 3. Create Loans Table (Handles Relationships)
CREATE TABLE IF NOT EXISTS loans (
    loan_id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER,
    member_id INTEGER,
    loan_date DATE DEFAULT CURRENT_DATE,
    return_date DATE,
    FOREIGN KEY (book_id) REFERENCES books(book_id) ON DELETE CASCADE,
    FOREIGN KEY (member_id) REFERENCES members(member_id) ON DELETE CASCADE
);

-- Insert Sample Data
INSERT OR IGNORE INTO books (title, author, isbn, available_copies) VALUES
('The Great Gatsby', 'F. Scott Fitzgerald', '9780743273565', 3),
('1984', 'George Orwell', '9780451524935', 2),
('To Kill a Mockingbird', 'Harper Lee', '9780061120084', 1);

INSERT OR IGNORE INTO members (name, email) VALUES
('Alice Smith', 'alice@email.com'),
('Bob Jones', 'bob@email.com');

INSERT OR IGNORE INTO loans (book_id, member_id, loan_date, return_date) VALUES
(1, 1, '2026-06-01', NULL);
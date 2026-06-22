# Library Management System

A Python-based CLI application for managing a library's books, members, and book loans, interacting seamlessly with a local SQLite database using relational modeling and foreign keys.

---

## How the System Design Works
The project uses a standard modular architecture separating data persistence from presentation:
* **`schema.sql`**: Defines a clean database schema containing tables for `books`, `members`, and a transitional relational table `loans` with cascaded foreign keys.
* **`database.py`**: Handles connection pools, query execution, constraints enforcement, and transactions (e.g., tracking stock counts during loans/returns).
* **`main.py`**: Houses the user-facing CLI presentation loop, taking inputs and reporting success or errors clearly.

---

## How to Install and Run the App

### 1. Prerequisites
Ensure you have Python 3.x installed.

### 2. Run the Application
Open a terminal in the project directory root and execute:
```bash
python main.py
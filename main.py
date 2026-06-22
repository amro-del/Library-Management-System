import os
from database import (
    init_db, add_book, list_books, update_book, delete_book,
    add_member, list_members, issue_loan, return_book, list_loans
)

def print_menu():
    print("\n" + "="*40)
    print("      LIBRARY MANAGEMENT SYSTEM")
    print("="*40)
    print("1. Add a Book")
    print("2. List All Books")
    print("3. Update a Book")
    print("4. Delete a Book")
    print("-" * 20)
    print("5. Add a Member")
    print("6. List All Members")
    print("-" * 20)
    print("7. Issue a Book Loan")
    print("8. Return a Book")
    print("9. List Active/Past Loans")
    print("-" * 20)
    print("0. Exit")
    print("="*40)

def main():
    # Automatically initialize the database on first run if it doesn't exist
    if not os.path.exists("library.db"):
        print("First time setup: Initializing library database...")
        init_db()

    while True:
        print_menu()
        choice = input("Enter your choice (0-9): ").strip()

        if choice == "1":
            title = input("Enter book title: ")
            author = input("Enter author: ")
            isbn = input("Enter ISBN: ")
            try:
                copies = int(input("Enter number of copies: "))
                if add_book(title, author, isbn, copies):
                    print("\n[Success] Book added successfully!")
            except ValueError:
                print("\n[Error] Invalid number for copies.")

        elif choice == "2":
            books = list_books()
            print("\n--- BOOKS LIST ---")
            print(f"{'ID':<5} {'Title':<25} {'Author':<20} {'ISBN':<15} {'Copies':<6}")
            print("-" * 75)
            for b in books:
                print(f"{b[0]:<5} {b[1]:<25} {b[2]:<20} {b[3]:<15} {b[4]:<6}")

        elif choice == "3":
            try:
                book_id = int(input("Enter Book ID to update: "))
                title = input("Enter new title: ")
                author = input("Enter new author: ")
                isbn = input("Enter new ISBN: ")
                copies = int(input("Enter new number of copies: "))
                if update_book(book_id, title, author, isbn, copies):
                    print("\n[Success] Book updated successfully!")
                else:
                    print("\n[Error] Book ID not found.")
            except ValueError:
                print("\n[Error] Invalid numeric input.")

        elif choice == "4":
            try:
                book_id = int(input("Enter Book ID to delete: "))
                if delete_book(book_id):
                    print("\n[Success] Book deleted successfully!")
                else:
                    print("\n[Error] Book ID not found.")
            except ValueError:
                print("\n[Error] Invalid Book ID.")

        elif choice == "5":
            name = input("Enter member name: ")
            email = input("Enter member email: ")
            if add_member(name, email):
                print("\n[Success] Member added successfully!")

        elif choice == "6":
            members = list_members()
            print("\n--- MEMBERS LIST ---")
            print(f"{'ID':<5} {'Name':<20} {'Email':<25} {'Join Date':<12}")
            print("-" * 65)
            for m in members:
                print(f"{m[0]:<5} {m[1]:<20} {m[2]:<25} {m[3]:<12}")

        elif choice == "7":
            try:
                book_id = int(input("Enter Book ID: "))
                member_id = int(input("Enter Member ID: "))
                if issue_loan(book_id, member_id):
                    print("\n[Success] Book checked out successfully!")
            except ValueError:
                print("\n[Error] Please enter valid IDs.")

        elif choice == "8":
            try:
                loan_id = int(input("Enter Loan ID to return: "))
                if return_book(loan_id):
                    print("\n[Success] Book returned successfully!")
            except ValueError:
                print("\n[Error] Invalid Loan ID.")

        elif choice == "9":
            loans = list_loans()
            print("\n--- LOAN HISTORY ---")
            print(f"{'Loan ID':<8} {'Book Title':<25} {'Member Name':<20} {'Loan Date':<12} {'Return Date':<12}")
            print("-" * 80)
            for l in loans:
                ret_date = l[4] if l[4] else "Active (Not Returned)"
                print(f"{l[0]:<8} {l[1]:<25} {l[2]:<20} {l[3]:<12} {ret_date:<12}")

        elif choice == "0":
            print("\nExiting application. Goodbye!")
            break
        else:
            print("\n[Error] Invalid option. Please try again.")

if __name__ == "__main__":
    main()
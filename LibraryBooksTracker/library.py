# Simple command-line library system
from datetime import date, timedelta

LOAN_DAYS = 14  # books are due 14 days after borrowing

books = []      # list of dictionaries, one per book
history = []    # list of text lines, one per borrow/return


def load_books():
    # each line in sample_data.txt: title,author,borrower,borrow_date
    file = open("sample_data.txt")
    for line in file:
        parts = line.strip().split(",")
        book = {
            "id": len(books) + 1,
            "title": parts[0],
            "author": parts[1],
            "available": True,
            "borrower": "",
            "borrow_date": "",
        }
        if parts[2] != "":
            book["available"] = False
            book["borrower"] = parts[2]
            book["borrow_date"] = parts[3]
        books.append(book)
    file.close()
3

def get_due_date(book):
    borrowed = date.fromisoformat(book["borrow_date"])
    return borrowed + timedelta(days=LOAN_DAYS)


def is_overdue(book):
    if book["available"] == False and date.today() > get_due_date(book):
        return True
    return False


def show_book(book):
    line = "[" + str(book["id"]) + "] " + book["title"] + " by " + book["author"]
    if book["available"]:
        line = line + " - Available"
    else:
        line = line + " - Borrowed by " + book["borrower"] + ", due " + str(get_due_date(book))
        if is_overdue(book):
            line = line + " (OVERDUE!)"
    print(line)


def add_book(title, author):
    if title == "" or author == "":
        print("Title and author can't be empty.")
        return
    new_book = {
        "id": len(books) + 1,
        "title": title,
        "author": author,
        "available": True,
        "borrower": "",
        "borrow_date": "",
    }
    books.append(new_book)
    print("Added " + title)


def search_books(word):
    found = False
    for book in books:
        if word.lower() in book["title"].lower() or word.lower() in book["author"].lower():
            show_book(book)
            found = True
    if found == False:
        print("No books found for '" + word + "'.")


def find_book(book_id):
    for book in books:
        if book["id"] == book_id:
            return book
    return None


def borrow_book(book_id, name):
    book = find_book(book_id)
    if book == None:
        print("There is no book with that ID.")
    elif name == "":
        print("Please enter a borrower name.")
    elif book["available"] == False:
        print("Sorry, '" + book["title"] + "' is already borrowed by " + book["borrower"] + ".")
    else:
        book["available"] = False
        book["borrower"] = name
        book["borrow_date"] = str(date.today())
        history.append(str(date.today()) + " BORROW " + book["title"] + " - " + name)
        print(name + " borrowed '" + book["title"] + "'. Due back " + str(get_due_date(book)))


def return_book(book_id):
    book = find_book(book_id)
    if book == None:
        print("There is no book with that ID.")
    elif book["available"]:
        print("That book wasn't borrowed, so it can't be returned.")
    else:
        note = "on time"
        if is_overdue(book):
            days_late = (date.today() - get_due_date(book)).days
            note = str(days_late) + " days late"
            print("Note: this book was " + note + "!")
        history.append(str(date.today()) + " RETURN " + book["title"] + " - " + book["borrower"] + " (" + note + ")")
        book["available"] = True
        book["borrower"] = ""
        book["borrow_date"] = ""
        print("Book returned. Thank you!")


def show_overdue():
    found = False
    for book in books:
        if is_overdue(book):
            show_book(book)
            found = True
    if found == False:
        print("No overdue books.")


def show_summary():
    total = len(books)
    borrowed = 0
    for book in books:
        if book["available"] == False:
            borrowed = borrowed + 1
    print("Total books:", total)
    print("Borrowed:", borrowed)
    print("Available:", total - borrowed)


def save_records():
    file = open("records.txt", "w")
    file.write("LIBRARY RECORDS - " + str(date.today()) + "\n\n")
    file.write("Activity this session:\n")
    if len(history) == 0:
        file.write("(nothing)\n")
    for line in history:
        file.write(line + "\n")
    file.write("\nCurrently borrowed:\n")
    for book in books:
        if book["available"] == False:
            text = book["title"] + " - " + book["borrower"] + " - due " + str(get_due_date(book))
            if is_overdue(book):
                text = text + " (OVERDUE)"
            file.write(text + "\n")
    file.close()
    print("Records saved to records.txt")


# ---------- main program ----------
load_books()
print("Welcome to the Library!")

while True:
    print()
    print("1. Show all books")
    print("2. Search")
    print("3. Add a book")
    print("4. Borrow a book")
    print("5. Return a book")
    print("6. Show overdue books")
    print("7. Summary")
    print("8. Save and quit")
    choice = input("Choose: ")

    if choice == "1":
        for book in books:
            show_book(book)
    elif choice == "2":
        search_books(input("Search for: "))
    elif choice == "3":
        add_book(input("Title: "), input("Author: "))
    elif choice == "4":
        id_text = input("Book ID: ")
        if id_text.isdigit():
            borrow_book(int(id_text), input("Your name: "))
        else:
            print("Please type a number.")
    elif choice == "5":
        id_text = input("Book ID: ")
        if id_text.isdigit():
            return_book(int(id_text))
        else:
            print("Please type a number.")
    elif choice == "6":
        show_overdue()
    elif choice == "7":
        show_summary()
    elif choice == "8":
        save_records()
        break
    else:
        print("Please choose 1-8.")

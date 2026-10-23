# Obstacle Log

1. **Dates were hard to compare.** I first stored dates as plain text like "2026-10-15" and couldn't tell if a book was late.
   Fix: used Python's `date` and `timedelta` (`date.fromisoformat()` to read, `+ timedelta(days=14)` for the due date).

2. **Program crashed when typing letters for a book ID.** `int("abc")` caused an error.
   Fix: check `id_text.isdigit()` first and print "Please type a number."

3. **Borrowing a book twice did nothing and gave no message.**
   Fix: added an `elif` that checks `available == False` and prints who has the book.

4. **Returning a book that wasn't borrowed.** It cleared the fields anyway.
   Fix: check if it is already available and print a message instead.

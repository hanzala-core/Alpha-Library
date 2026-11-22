"""Book catalogue operations and input validation."""
import sqlite3


BOOK_HEADERS = ("ID", "Title", "Author", "ISBN", "Category", "Available / Total")


def clean_isbn(value):
    """Normalize a 10- or 13-digit ISBN (spaces and hyphens accepted)."""
    isbn = str(value).replace("-", "").replace(" ", "").strip()
    if len(isbn) not in (10, 13) or not isbn.isascii() or not isbn.isdigit():
        raise ValueError("ISBN must contain exactly 10 or 13 digits")
    return isbn


def validate_book(conn, title, author, isbn, category, copies, *, exclude_id=None):
    title, author = str(title).strip(), str(author).strip()
    category = str(category).strip() or "General"
    isbn = clean_isbn(isbn)
    if not title or not author:
        raise ValueError("Title and author are required")
    if isinstance(copies, bool):
        raise ValueError("Copies must be a positive integer")
    try:
        copies = int(copies)
    except (TypeError, ValueError) as exc:
        raise ValueError("Copies must be a positive integer") from exc
    if copies < 1:
        raise ValueError("Copies must be at least 1")
    duplicate = conn.execute("SELECT id FROM books WHERE isbn = ?", (isbn,)).fetchone()
    if duplicate is not None and duplicate["id"] != exclude_id:
        raise ValueError("ISBN already exists in the catalogue")
    return {
        "title": title, "author": author, "isbn": isbn,
        "category": category, "total_copies": copies,
    }


def add_book(conn, title, author, isbn, category="General", copies=1):
    data = validate_book(conn, title, author, isbn, category, copies)
    cur = conn.execute(
        """INSERT INTO books (title, author, isbn, category, total_copies)
           VALUES (:title, :author, :isbn, :category, :total_copies)""", data
    )
    conn.commit()
    return cur.lastrowid


def list_books(conn):
    """Return catalogue entries, sorted by title, with computed availability."""
    rows = conn.execute("""
        SELECT b.id, b.title, b.author, b.isbn, b.category, b.total_copies,
               b.total_copies - COUNT(l.id) AS available
        FROM books AS b
        LEFT JOIN loans AS l ON l.book_id = b.id AND l.returned_at IS NULL
        GROUP BY b.id
        ORDER BY LOWER(b.title), b.id
    """).fetchall()
    return [dict(row) for row in rows]


def get_book(conn, book_id):
    for book in list_books(conn):
        if book["id"] == int(book_id):
            return book
    raise ValueError("Book not found")


def book_rows(conn):
    return [
        (b["id"], b["title"], b["author"], b["isbn"], b["category"],
         f'{b["available"]} / {b["total_copies"]}')
        for b in list_books(conn)
    ]


def edit_book(conn, book_id, *, title=None, author=None, isbn=None, category=None, copies=None):
    old = get_book(conn, book_id)
    data = validate_book(
        conn, title if title is not None else old["title"],
        author if author is not None else old["author"],
        isbn if isbn is not None else old["isbn"],
        category if category is not None else old["category"],
        copies if copies is not None else old["total_copies"],
        exclude_id=old["id"],
    )
    outstanding = old["total_copies"] - old["available"]
    if data["total_copies"] < outstanding:
        raise ValueError("Copies cannot be fewer than books currently on loan")
    conn.execute(
        """UPDATE books SET title=:title, author=:author, isbn=:isbn,
           category=:category, total_copies=:total_copies WHERE id=:id""",
        {**data, "id": old["id"]},
    )
    conn.commit()
    return get_book(conn, old["id"])


def delete_book(conn, book_id, *, confirm=False):
    if not confirm:
        raise ValueError("Deletion requires explicit confirmation")
    book = get_book(conn, book_id)
    if book["available"] < book["total_copies"]:
        raise ValueError("Cannot delete a book while copies are on loan")
    # Retain historical loan records; do not cascade-delete loan history.
    prior_loans = conn.execute(
        "SELECT COUNT(*) FROM loans WHERE book_id = ?", (book["id"],)
    ).fetchone()[0]
    if prior_loans:
        raise ValueError("Cannot delete a book with loan history")
    conn.execute("DELETE FROM books WHERE id = ?", (book["id"],))
    conn.commit()
    return True


def search_books(conn, term):
    """Case-insensitive literal substring search (including % and _)."""
    term = str(term).strip().lower()
    if not term:
        return []
    result = []
    for book in list_books(conn):
        if any(term in str(book[field]).lower()
               for field in ("title", "author", "isbn", "category")):
            result.append(book)
    return result

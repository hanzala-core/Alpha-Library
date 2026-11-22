"""Issue and return books while enforcing availability."""
from datetime import date
from library.catalog import get_book


def issue_book(conn, book_id, member_id):
    book = get_book(conn, book_id)
    if conn.execute("SELECT id FROM members WHERE id = ?", (member_id,)).fetchone() is None:
        raise ValueError("Member not found")
    if book["available"] <= 0:
        raise ValueError("No copies of this book are available")
    cur = conn.execute(
        "INSERT INTO loans (book_id, member_id, issued_at) VALUES (?, ?, ?)",
        (book_id, member_id, date.today().isoformat()),
    )
    conn.commit()
    return cur.lastrowid


def return_book(conn, loan_id):
    loan = conn.execute(
        "SELECT id FROM loans WHERE id=? AND returned_at IS NULL", (loan_id,)
    ).fetchone()
    if loan is None:
        raise ValueError("Active loan not found")
    conn.execute(
        "UPDATE loans SET returned_at=? WHERE id=?",
        (date.today().isoformat(), loan_id)
    )
    conn.commit()
    return True


def list_active_loans(conn):
    rows = conn.execute("""
        SELECT l.id, b.title, m.name AS member, l.issued_at
        FROM loans l
        JOIN books b ON b.id=l.book_id
        JOIN members m ON m.id=l.member_id
        WHERE l.returned_at IS NULL
        ORDER BY l.id
    """).fetchall()
    return [dict(row) for row in rows]

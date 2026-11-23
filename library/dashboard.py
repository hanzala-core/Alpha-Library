"""Read-only library dashboard and explicitly confirmed demo-data reset."""
from library.loans import list_overdue_loans

SAMPLE_BOOKS = (
    ("Python Basics", "A. Writer", "9780000000001", "Technology", 2),
    ("The Library", "B. Author", "9780000000002", "Fiction", 1),
)
SAMPLE_MEMBERS = (("Sample Member", "sample.member@example.test"),)


def dashboard_data(conn, *, as_of=None):
    """Return dashboard counts and the overdue-loan detail list."""
    book_titles = conn.execute(
        "SELECT COUNT(*) FROM books WHERE is_active=1"
    ).fetchone()[0]
    registered_members = conn.execute(
        "SELECT COUNT(*) FROM members WHERE is_active=1"
    ).fetchone()[0]
    active_loans = conn.execute(
        "SELECT COUNT(*) FROM loans WHERE returned_at IS NULL"
    ).fetchone()[0]
    overdue = list_overdue_loans(conn, as_of=as_of)
    return {
        "book_titles": book_titles,
        "registered_members": registered_members,
        "active_loans": active_loans,
        "overdue_loans": len(overdue),
        "overdue_list": overdue,
    }


def reset_sample_data(conn, *, confirm=False):
    """Replace database contents with demo fixtures only after explicit confirmation.

    This is intentionally destructive, so the caller must display a confirmation
    prompt. Existing SQLite data is otherwise never changed by application upgrades.
    """
    if confirm is not True:
        raise ValueError("Sample-data reset requires explicit confirmation")
    try:
        conn.execute("BEGIN IMMEDIATE")
        conn.execute("DELETE FROM loans")
        conn.execute("DELETE FROM books")
        conn.execute("DELETE FROM members")
        conn.executemany(
            "INSERT INTO books (title, author, isbn, category, total_copies) VALUES (?, ?, ?, ?, ?)",
            SAMPLE_BOOKS,
        )
        conn.executemany(
            "INSERT INTO members (name, email) VALUES (?, ?)", SAMPLE_MEMBERS
        )
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    return dashboard_data(conn)

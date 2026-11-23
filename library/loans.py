"""Issue, return and report book loans with due dates and fines."""
from datetime import date, datetime, timedelta

from library.catalog import get_book

LOAN_DAYS = 14
FINE_PER_DAY = 10


def _as_date(value, field_name="date"):
    if value is None:
        return date.today()
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    try:
        return date.fromisoformat(str(value))
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{field_name} must be a valid ISO date") from exc


def days_late(due_date, as_of=None):
    """Return the number of calendar days past due, never less than zero."""
    return max(0, (_as_date(as_of) - _as_date(due_date, "due_date")).days)


def fine_for(due_date, as_of=None):
    """Return the overdue fine in rupees (Rs 10 for each late day)."""
    return days_late(due_date, as_of) * FINE_PER_DAY


def is_overdue(due_date, as_of=None):
    """Whether a loan is past its due date on the supplied/current date."""
    return days_late(due_date, as_of) > 0


def issue_book(conn, book_id, member_id, *, issued_at=None):
    """Issue one available copy; a member may have at most three active loans."""
    issued = _as_date(issued_at, "issued_at")
    due = issued + timedelta(days=LOAN_DAYS)
    try:
        # Serialise the checks and insert so concurrent issuances cannot exceed limits.
        conn.execute("BEGIN IMMEDIATE")
        book = get_book(conn, book_id)
        if conn.execute(
            "SELECT id FROM members WHERE id = ? AND is_active=1", (member_id,)
        ).fetchone() is None:
            raise ValueError("Member not found")
        active_count = conn.execute(
            "SELECT COUNT(*) FROM loans WHERE member_id=? AND returned_at IS NULL",
            (member_id,),
        ).fetchone()[0]
        if active_count >= 3:
            raise ValueError("A member may have at most 3 active loans")
        if conn.execute(
            "SELECT 1 FROM loans WHERE book_id=? AND member_id=? AND returned_at IS NULL",
            (book_id, member_id),
        ).fetchone():
            raise ValueError("This member already has an active loan for this book")
        if book["available"] <= 0:
            raise ValueError("No copies of this book are available")
        cur = conn.execute(
            "INSERT INTO loans (book_id, member_id, issued_at, due_date) VALUES (?, ?, ?, ?)",
            (book_id, member_id, issued.isoformat(), due.isoformat()),
        )
        conn.commit()
        return cur.lastrowid
    except Exception:
        conn.rollback()
        raise


def return_book(conn, loan_id, *, returned_at=None):
    """Return an active loan by ID and report its final overdue days and fine."""
    returned = _as_date(returned_at, "returned_at")
    loan = conn.execute(
        """SELECT id, COALESCE(due_date, date(issued_at, '+14 days')) AS due_date
           FROM loans WHERE id=? AND returned_at IS NULL""",
        (loan_id,),
    ).fetchone()
    if loan is None:
        raise ValueError("Active loan not found")
    late_days = days_late(loan["due_date"], returned)
    amount = late_days * FINE_PER_DAY
    conn.execute("UPDATE loans SET returned_at=? WHERE id=? AND returned_at IS NULL",
                 (returned.isoformat(), loan_id))
    if conn.execute("SELECT changes()").fetchone()[0] != 1:
        conn.rollback()
        raise ValueError("Active loan not found")
    conn.commit()
    return {"loan_id": loan_id, "returned_at": returned.isoformat(),
            "days_late": late_days, "fine": amount}


def list_loans(conn, *, include_returned=False, as_of=None):
    """List active loans, or all loans when include_returned is requested."""
    where = "" if include_returned else "WHERE l.returned_at IS NULL"
    rows = conn.execute(f"""
        SELECT l.id, l.book_id, l.member_id, b.title, m.name AS member,
               l.issued_at, COALESCE(l.due_date, date(l.issued_at, '+14 days')) AS due_date,
               l.returned_at
        FROM loans l
        JOIN books b ON b.id=l.book_id
        JOIN members m ON m.id=l.member_id
        {where}
        ORDER BY l.id
    """).fetchall()
    result = []
    for row in rows:
        item = dict(row)
        item["status"] = "returned" if item["returned_at"] is not None else "active"
        item["days_late"] = days_late(item["due_date"], as_of) if item["status"] == "active" else days_late(item["due_date"], item["returned_at"])
        item["fine"] = item["days_late"] * FINE_PER_DAY
        item["overdue"] = item["status"] == "active" and item["days_late"] > 0
        result.append(item)
    return result


def list_active_loans(conn, *, as_of=None):
    """Backward-compatible active-loan listing."""
    return list_loans(conn, as_of=as_of)


def list_overdue_loans(conn, *, as_of=None):
    """List active overdue loans with current days late and fines."""
    return [loan for loan in list_loans(conn, as_of=as_of) if loan["overdue"]]

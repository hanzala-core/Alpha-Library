"""Library member records and safe removal."""
import re

EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


def validate_member(conn, name, email):
    name = str(name).strip()
    email = str(email).strip().lower()
    if not name:
        raise ValueError("Member name is required")
    if not EMAIL_RE.fullmatch(email):
        raise ValueError("Enter a valid email address")
    if conn.execute("SELECT 1 FROM members WHERE email = ? AND is_active = 1", (email,)).fetchone():
        raise ValueError("Member email already registered")
    return name, email


def register_member(conn, name, email):
    name, email = validate_member(conn, name, email)
    archived = conn.execute(
        "SELECT id FROM members WHERE email = ? AND is_active = 0", (email,)
    ).fetchone()
    if archived is not None:
        conn.execute(
            "UPDATE members SET name=?, is_active=1 WHERE id=?",
            (name, archived["id"]),
        )
        conn.commit()
        return archived["id"]
    cur = conn.execute(
        "INSERT INTO members (name, email) VALUES (?, ?)", (name, email)
    )
    conn.commit()
    return cur.lastrowid


def list_members(conn):
    rows = conn.execute("""
        SELECT m.id, m.name, m.email, COUNT(l.id) AS active_loans
        FROM members AS m
        LEFT JOIN loans AS l ON l.member_id = m.id AND l.returned_at IS NULL
        WHERE m.is_active = 1
        GROUP BY m.id ORDER BY LOWER(m.name), m.id
    """).fetchall()
    return [dict(row) for row in rows]


def remove_member(conn, member_id, *, confirm=False):
    if not confirm:
        raise ValueError("Removal requires explicit confirmation")
    member = conn.execute(
        "SELECT id FROM members WHERE id = ? AND is_active = 1", (member_id,)
    ).fetchone()
    if member is None:
        raise ValueError("Member not found")
    active = conn.execute(
        "SELECT COUNT(*) FROM loans WHERE member_id=? AND returned_at IS NULL",
        (member_id,)
    ).fetchone()[0]
    if active:
        raise ValueError("Cannot remove a member with books on loan")
    # Soft deletion allows removal after return without deleting loan history.
    conn.execute("UPDATE members SET is_active=0 WHERE id=?", (member_id,))
    conn.commit()
    return True

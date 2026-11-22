"""SQLite storage and database initialization."""
import sqlite3
from pathlib import Path


def connect(path="alpha_library.db"):
    """Open a SQLite connection and ensure that the schema is present."""
    if str(path) != ":memory:":
        Path(path).expanduser().resolve().parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            isbn TEXT NOT NULL UNIQUE,
            category TEXT NOT NULL DEFAULT 'General',
            total_copies INTEGER NOT NULL CHECK (total_copies >= 1),
            is_active INTEGER NOT NULL DEFAULT 1 CHECK (is_active IN (0, 1))
        );
        CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            is_active INTEGER NOT NULL DEFAULT 1 CHECK (is_active IN (0, 1))
        );
        CREATE TABLE IF NOT EXISTS loans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER NOT NULL REFERENCES books(id),
            member_id INTEGER NOT NULL REFERENCES members(id),
            issued_at TEXT NOT NULL,
            returned_at TEXT,
            CHECK (returned_at IS NULL OR returned_at >= issued_at)
        );
        CREATE INDEX IF NOT EXISTS idx_loans_book_active ON loans(book_id, returned_at);
        CREATE INDEX IF NOT EXISTS idx_loans_member_active ON loans(member_id, returned_at);
    """)
    # Add archive flags to databases created by earlier prototype versions.
    for table in ("books", "members"):
        columns = {row["name"] for row in conn.execute(f"PRAGMA table_info({table})")}
        if "is_active" not in columns:
            conn.execute(
                f"ALTER TABLE {table} ADD COLUMN is_active INTEGER NOT NULL DEFAULT 1"
            )
    conn.commit()
    return conn

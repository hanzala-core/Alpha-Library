# Implementation notes: handout alignment and SQLite integration

The handout's Appendix A uses a small offline Python application organized around `storage.py`, `books.py`, `members.py`, `loans.py`, `dashboard.py`, JSON sample data and `test_library.py`. This integration prototype implements the same borrowing, return, fine and dashboard outcomes using the existing modular `library/` package, a numbered CLI, and SQLite.

## Architectural differences

- **Storage:** SQLite replaces `library_data.json`. The schema is upgraded in place: the new nullable `loans.due_date` column is added to existing databases and backfilled as issue date + 14 days. Existing books, members, loan history and IDs are preserved during upgrade.
- **Modules/tests:** Existing `catalog.py` serves the book operations; `database.py` provides persistence; `members.py`, `loans.py`, and the new `dashboard.py` keep responsibilities separate. Tests remain split across `tests/` rather than one `test_library.py`.
- **Interface:** Features use the current interactive CLI. They do not reproduce the handout's exact screen layout or its JSON file workflow.
- **Reset:** The confirmed reset action intentionally replaces all current books, members and loans with the two-book/one-member demonstration fixture. Declining confirmation changes nothing. This is separate from application startup and schema migration, neither of which deletes data.
- **Loan restriction:** The integration prototype defines the handout's same-copy rule as preventing the same member from holding another active loan for the same book title, while allowing different members to borrow separate copies.

This is a technical implementation adaptation, not evidence that the Scrum team completed individual assigned story work, human review, Product Owner acceptance, or sprint events. No stories are closed by these changes.

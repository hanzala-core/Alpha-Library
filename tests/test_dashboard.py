"""Dashboard counts, overdue reporting and guarded sample reset tests."""
import unittest
from library.catalog import add_book
from library.dashboard import dashboard_data, reset_sample_data
from library.database import connect
from library.loans import issue_book, return_book
from library.members import register_member


class DashboardTests(unittest.TestCase):
    def setUp(self):
        self.db = connect(":memory:")

    def tearDown(self):
        self.db.close()

    def test_empty_dashboard_counts(self):
        self.assertEqual(dashboard_data(self.db), {
            "book_titles": 0, "registered_members": 0, "active_loans": 0,
            "overdue_loans": 0, "overdue_list": [],
        })

    def test_counts_only_active_records_and_overdue_loans(self):
        book = add_book(self.db, "Dash book", "Writer", "1234500000", copies=2)
        member = register_member(self.db, "Dash Member", "dash@example.com")
        overdue = issue_book(self.db, book, member, issued_at="2025-01-01")
        on_time = add_book(self.db, "Other book", "Writer", "1234500001", copies=1)
        issue_book(self.db, on_time, member, issued_at="2025-01-10")
        data = dashboard_data(self.db, as_of="2025-01-20")
        self.assertEqual((data["book_titles"], data["registered_members"],
                          data["active_loans"], data["overdue_loans"]), (2, 1, 2, 1))
        self.assertEqual(data["overdue_list"][0]["id"], overdue)
        self.assertEqual(data["overdue_list"][0]["fine"], 50)
        return_book(self.db, overdue, returned_at="2025-01-20")
        self.assertEqual(dashboard_data(self.db, as_of="2025-01-20")["overdue_loans"], 0)

    def test_reset_requires_explicit_confirmation_and_preserves_without_call(self):
        add_book(self.db, "Keep me", "Writer", "1234500002")
        with self.assertRaisesRegex(ValueError, "confirmation"):
            reset_sample_data(self.db)
        self.assertEqual(dashboard_data(self.db)["book_titles"], 1)

    def test_confirmed_reset_replaces_records_with_sample_fixture(self):
        add_book(self.db, "Old book", "Writer", "1234500003")
        register_member(self.db, "Old Member", "old@example.com")
        result = reset_sample_data(self.db, confirm=True)
        self.assertEqual(result["book_titles"], 2)
        self.assertEqual(result["registered_members"], 1)
        self.assertEqual(result["active_loans"], 0)
        self.assertEqual(self.db.execute("SELECT title FROM books WHERE is_active=1 ORDER BY id").fetchall()[0][0], "Python Basics")


if __name__ == "__main__":
    unittest.main()

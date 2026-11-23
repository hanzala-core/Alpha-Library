"""Loan acceptance and regression tests, including date/fine boundaries."""
import unittest
from datetime import date

from library.catalog import add_book, get_book
from library.database import connect
from library.loans import (
    days_late, fine_for, is_overdue, issue_book, list_active_loans,
    list_loans, return_book,
)
from library.members import list_members, register_member, remove_member


class MembersAndLoansTests(unittest.TestCase):
    def setUp(self):
        self.db = connect(":memory:")
        self.book = add_book(self.db, "Algorithms", "B. Author", "1234567890", copies=4)
        self.member_id = register_member(self.db, "Member One", "member@example.com")

    def tearDown(self):
        self.db.close()

    def member(self, email="member@example.com"):
        return register_member(self.db, "Member One", email)

    def test_register_member(self):
        self.assertEqual(list_members(self.db)[0]["email"], "member@example.com")
        self.assertGreater(self.member_id, 0)

    def test_duplicate_email_case_insensitive(self):
        with self.assertRaisesRegex(ValueError, "already registered"):
            self.member("MEMBER@example.com")

    def test_invalid_email_or_name(self):
        for name, email in [("", "a@example.com"), ("Ali", "bad"),
                            ("Ali", "a@"), ("Ali", "a b@c.com")]:
            with self.subTest(name=name, email=email), self.assertRaises(ValueError):
                register_member(self.db, name, email)

    def test_issue_due_exactly_fourteen_days(self):
        loan_id = issue_book(self.db, self.book, self.member_id,
                             issued_at=date(2025, 1, 1))
        loan = list_active_loans(self.db)[0]
        self.assertEqual(loan["id"], loan_id)
        self.assertEqual(loan["due_date"], "2025-01-15")

    def test_issue_book_decrements_availability_and_returns_id(self):
        issue_book(self.db, self.book, self.member_id)
        self.assertEqual(get_book(self.db, self.book)["available"], 3)

    def test_cannot_issue_when_no_copies_available(self):
        one_copy = add_book(self.db, "Single", "Writer", "1234567891", copies=1)
        issue_book(self.db, one_copy, self.member_id)
        second_member = register_member(self.db, "Another Member", "second@example.com")
        # Use a different member to isolate out-of-stock from the duplicate-loan rule.
        with self.assertRaisesRegex(ValueError, "No copies"):
            issue_book(self.db, one_copy, second_member)
        self.assertEqual(get_book(self.db, one_copy)["available"], 0)

    def test_member_maximum_three_active_loans_boundary(self):
        for i in range(3):
            book = add_book(self.db, f"Book {i}", "Writer", f"12345678{i}0", copies=1)
            issue_book(self.db, book, self.member_id)
        with self.assertRaisesRegex(ValueError, "at most 3"):
            issue_book(self.db, self.book, self.member_id)
        self.assertEqual(list_members(self.db)[0]["active_loans"], 3)

    def test_returned_loan_does_not_count_toward_three_limit(self):
        loan = issue_book(self.db, self.book, self.member_id)
        return_book(self.db, loan)
        for i in range(3):
            book = add_book(self.db, f"Book {i}", "Writer", f"98765432{i}0", copies=1)
            issue_book(self.db, book, self.member_id)
        self.assertEqual(list_members(self.db)[0]["active_loans"], 3)

    def test_duplicate_active_same_book_member_rejected_even_with_copies(self):
        issue_book(self.db, self.book, self.member_id)
        with self.assertRaisesRegex(ValueError, "already has an active loan"):
            issue_book(self.db, self.book, self.member_id)
        self.assertEqual(get_book(self.db, self.book)["available"], 3)

    def test_unknown_member_or_book_rejected(self):
        with self.assertRaisesRegex(ValueError, "Member not found"):
            issue_book(self.db, self.book, 9999)
        with self.assertRaisesRegex(ValueError, "Book not found"):
            issue_book(self.db, 9999, self.member_id)

    def test_list_defaults_to_active_and_can_include_returned(self):
        loan_id = issue_book(self.db, self.book, self.member_id)
        return_book(self.db, loan_id)
        self.assertEqual(list_loans(self.db), [])
        all_loans = list_loans(self.db, include_returned=True)
        self.assertEqual(len(all_loans), 1)
        self.assertEqual(all_loans[0]["status"], "returned")

    def test_return_by_loan_id_restores_availability_and_prevents_duplicate(self):
        loan_id = issue_book(self.db, self.book, self.member_id)
        result = return_book(self.db, loan_id)
        self.assertEqual(result["fine"], 0)
        self.assertEqual(get_book(self.db, self.book)["available"], 4)
        with self.assertRaisesRegex(ValueError, "Active loan not found"):
            return_book(self.db, loan_id)

    def test_days_late_and_fine_boundaries(self):
        due = "2025-02-14"
        self.assertEqual(days_late(due, "2025-02-13"), 0)
        self.assertEqual(days_late(due, due), 0)
        self.assertFalse(is_overdue(due, due))
        self.assertEqual(fine_for(due, due), 0)
        self.assertEqual(days_late(due, "2025-02-15"), 1)
        self.assertTrue(is_overdue(due, "2025-02-15"))
        self.assertEqual(fine_for(due, "2025-02-15"), 10)
        self.assertEqual(fine_for(due, "2025-02-17"), 30)

    def test_invalid_date_is_rejected(self):
        for fn in (days_late, fine_for, is_overdue):
            with self.subTest(fn=fn.__name__), self.assertRaises(ValueError):
                fn("not-a-date")

    def test_return_late_calculates_final_fine(self):
        loan_id = issue_book(self.db, self.book, self.member_id,
                             issued_at="2025-01-01")
        result = return_book(self.db, loan_id, returned_at="2025-01-18")
        self.assertEqual(result["days_late"], 3)
        self.assertEqual(result["fine"], 30)

    def test_active_loan_listing_shows_overdue_days_and_fine(self):
        issue_book(self.db, self.book, self.member_id, issued_at="2025-01-01")
        row = list_active_loans(self.db, as_of="2025-01-18")[0]
        self.assertTrue(row["overdue"])
        self.assertEqual(row["days_late"], 3)
        self.assertEqual(row["fine"], 30)

    def test_remove_member_confirmation_and_active_loan_constraints(self):
        with self.assertRaisesRegex(ValueError, "confirmation"):
            remove_member(self.db, self.member_id)
        loan = issue_book(self.db, self.book, self.member_id)
        with self.assertRaisesRegex(ValueError, "on loan"):
            remove_member(self.db, self.member_id, confirm=True)
        return_book(self.db, loan)
        self.assertTrue(remove_member(self.db, self.member_id, confirm=True))
        self.assertEqual(list_members(self.db), [])
        self.assertEqual(self.db.execute(
            "SELECT COUNT(*) FROM loans WHERE member_id=?", (self.member_id,)
        ).fetchone()[0], 1)


if __name__ == "__main__":
    unittest.main()

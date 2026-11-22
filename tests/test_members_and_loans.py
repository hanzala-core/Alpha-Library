"""Registration, borrowing and safe-removal tests."""
import unittest
from library.database import connect
from library.catalog import add_book, get_book
from library.members import list_members, register_member, remove_member
from library.loans import issue_book, list_active_loans, return_book


class MembersAndLoansTests(unittest.TestCase):
    def setUp(self):
        self.db = connect(":memory:")
        self.book = add_book(self.db, "Algorithms", "B. Author", "1234567890", copies=1)

    def tearDown(self):
        self.db.close()

    def member(self, email="member@example.com"):
        return register_member(self.db, "Member One", email)

    def test_register_member(self):
        id = self.member("MEMBER@EXAMPLE.COM")
        self.assertEqual(list_members(self.db)[0]["email"], "member@example.com")
        self.assertGreater(id, 0)

    def test_duplicate_email_case_insensitive(self):
        self.member()
        with self.assertRaisesRegex(ValueError, "already registered"):
            self.member("MEMBER@example.com")

    def test_invalid_email_or_name(self):
        for name, email in [("", "a@example.com"), ("Ali", "bad"),
                            ("Ali", "a@"), ("Ali", "a b@c.com")]:
            with self.subTest(name=name, email=email), self.assertRaises(ValueError):
                register_member(self.db, name, email)

    def test_issue_book(self):
        mid = self.member()
        loan = issue_book(self.db, self.book, mid)
        self.assertEqual(get_book(self.db, self.book)["available"], 0)
        self.assertEqual(list_active_loans(self.db)[0]["id"], loan)

    def test_cannot_issue_unavailable_book(self):
        mid = self.member()
        issue_book(self.db, self.book, mid)
        with self.assertRaisesRegex(ValueError, "No copies"):
            issue_book(self.db, self.book, mid)

    def test_unknown_member_cannot_borrow(self):
        with self.assertRaisesRegex(ValueError, "Member not found"):
            issue_book(self.db, self.book, 9999)

    def test_unknown_book_cannot_borrow(self):
        with self.assertRaisesRegex(ValueError, "Book not found"):
            issue_book(self.db, 9999, self.member())

    def test_return_book(self):
        loan = issue_book(self.db, self.book, self.member())
        self.assertTrue(return_book(self.db, loan))
        self.assertEqual(list_active_loans(self.db), [])
        self.assertEqual(get_book(self.db, self.book)["available"], 1)

    def test_cannot_return_twice(self):
        loan = issue_book(self.db, self.book, self.member())
        return_book(self.db, loan)
        with self.assertRaisesRegex(ValueError, "Active loan not found"):
            return_book(self.db, loan)

    def test_remove_member_confirm_required(self):
        mid = self.member()
        with self.assertRaisesRegex(ValueError, "confirmation"):
            remove_member(self.db, mid)
        self.assertEqual(len(list_members(self.db)), 1)

    def test_remove_member_no_loans(self):
        mid = self.member()
        self.assertTrue(remove_member(self.db, mid, confirm=True))
        self.assertEqual(list_members(self.db), [])

    def test_cannot_remove_with_active_loans(self):
        mid = self.member()
        issue_book(self.db, self.book, mid)
        with self.assertRaisesRegex(ValueError, "on loan"):
            remove_member(self.db, mid, confirm=True)

    def test_remove_member_after_return_preserves_history(self):
        mid = self.member()
        loan = issue_book(self.db, self.book, mid)
        return_book(self.db, loan)
        self.assertTrue(remove_member(self.db, mid, confirm=True))
        self.assertEqual(list_members(self.db), [])
        self.assertEqual(self.db.execute(
            "SELECT COUNT(*) FROM loans WHERE member_id=?", (mid,)
        ).fetchone()[0], 1)

    def test_archived_email_can_be_reregistered(self):
        mid = self.member()
        remove_member(self.db, mid, confirm=True)
        self.assertEqual(register_member(self.db, "New Name", "member@example.com"), mid)
        self.assertEqual(list_members(self.db)[0]["name"], "New Name")

    def test_member_loan_count(self):
        mid = self.member()
        issue_book(self.db, self.book, mid)
        self.assertEqual(list_members(self.db)[0]["active_loans"], 1)


if __name__ == "__main__":
    unittest.main()

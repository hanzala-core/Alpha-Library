"""Catalogue and ISBN regression tests."""
import unittest
from library.database import connect
from library.catalog import (
    add_book, book_rows, clean_isbn, delete_book, edit_book,
    get_book, list_books, search_books,
)
from library.members import register_member
from library.loans import issue_book, return_book


class CatalogueTests(unittest.TestCase):
    def setUp(self):
        self.db = connect(":memory:")

    def tearDown(self):
        self.db.close()

    def add(self, **kwargs):
        data = dict(title="Python Basics", author="A. Writer", isbn="9781234567890",
                    category="Technology", copies=2)
        data.update(kwargs)
        return add_book(self.db, **data)

    def test_add_book_and_normalize_isbn(self):
        book = get_book(self.db, self.add(isbn="978-1234567890"))
        self.assertEqual(book["isbn"], "9781234567890")
        self.assertEqual(book["available"], 2)

    def test_clean_isbn_accepts_ten_digits(self):
        self.assertEqual(clean_isbn("12-3456 7890"), "1234567890")

    def test_invalid_isbn(self):
        for bad in ["invalid", "12345678", "123456789X", ""]:
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                self.add(isbn=bad)

    def test_required_fields_and_positive_copies(self):
        for changes in [{"title": " "}, {"author": ""}, {"copies": 0},
                        {"copies": -1}, {"copies": "abc"}]:
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                self.add(**changes)

    def test_duplicate_normalized_isbn(self):
        self.add()
        with self.assertRaisesRegex(ValueError, "already exists"):
            self.add(isbn="978-1234567890")

    def test_sorting_and_book_rows(self):
        self.add(title="Zebra")
        self.add(title="alpha", isbn="1234567890")
        self.assertEqual([b["title"] for b in list_books(self.db)], ["alpha", "Zebra"])
        self.assertEqual(len(book_rows(self.db)), 2)

    def test_edit_book(self):
        id = self.add()
        changed = edit_book(self.db, id, title="Python Advanced", copies=3)
        self.assertEqual(changed["title"], "Python Advanced")
        self.assertEqual(changed["total_copies"], 3)

    def test_edit_duplicate_isbn_rejected(self):
        id = self.add()
        self.add(isbn="1234567890")
        with self.assertRaisesRegex(ValueError, "already exists"):
            edit_book(self.db, id, isbn="1234567890")

    def test_edit_cannot_reduce_copies_below_active_loans(self):
        id = self.add()
        member = register_member(self.db, "Ayesha", "a@example.com")
        issue_book(self.db, id, member)
        issue_book(self.db, id, member)
        with self.assertRaisesRegex(ValueError, "on loan"):
            edit_book(self.db, id, copies=1)

    def test_available_counts_and_return(self):
        id = self.add()
        member = register_member(self.db, "Ayesha", "a@example.com")
        loan = issue_book(self.db, id, member)
        self.assertEqual(get_book(self.db, id)["available"], 1)
        return_book(self.db, loan)
        self.assertEqual(get_book(self.db, id)["available"], 2)

    def test_delete_requires_confirmation(self):
        id = self.add()
        with self.assertRaisesRegex(ValueError, "confirmation"):
            delete_book(self.db, id)
        self.assertEqual(len(list_books(self.db)), 1)

    def test_delete_empty_book(self):
        id = self.add()
        self.assertTrue(delete_book(self.db, id, confirm=True))
        self.assertEqual(list_books(self.db), [])

    def test_delete_blocked_with_active_loan(self):
        id = self.add()
        member = register_member(self.db, "Ayesha", "a@example.com")
        issue_book(self.db, id, member)
        with self.assertRaisesRegex(ValueError, "on loan"):
            delete_book(self.db, id, confirm=True)

    def test_delete_with_historical_loan_blocked(self):
        id = self.add()
        member = register_member(self.db, "Ayesha", "a@example.com")
        loan = issue_book(self.db, id, member)
        return_book(self.db, loan)
        with self.assertRaisesRegex(ValueError, "loan history"):
            delete_book(self.db, id, confirm=True)

    def test_search_all_fields_case_insensitive(self):
        self.add()
        for term in ["PYTHON", "writer", "9781234567890", "technology"]:
            with self.subTest(term=term):
                self.assertEqual(len(search_books(self.db, term)), 1)
        self.assertEqual(search_books(self.db, "No Match"), [])
        self.assertEqual(search_books(self.db, ""), [])

    def test_not_found(self):
        with self.assertRaisesRegex(ValueError, "not found"):
            get_book(self.db, 9)


if __name__ == "__main__":
    unittest.main()

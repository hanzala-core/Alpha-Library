"""A small CLI smoke test with injected I/O."""
import unittest
from library.database import connect
from library.ui import LibraryCLI, render_table


class CLITests(unittest.TestCase):
    def setUp(self):
        self.db = connect(":memory:")

    def tearDown(self):
        self.db.close()

    def test_table_renders_no_rows(self):
        self.assertIn("Title", render_table(("Title",), []))

    def test_add_list_search_quit(self):
        inputs = iter([
            "1", "My Book", "Test Author", "9781234567890", "Fiction", "2",
            "2", "5", "my book", "0",
        ])
        out = []
        LibraryCLI(self.db, input_fn=lambda _: next(inputs), output_fn=out.append).run()
        combined = "\n".join(out)
        self.assertIn("Added book #", combined)
        self.assertIn("My Book", combined)
        self.assertIn("2 / 2", combined)
        self.assertIn("Goodbye", combined)

    def test_cancel_delete(self):
        inputs = iter(["1", "My Book", "Test Author", "9781234567890",
                       "Fiction", "1", "4", "1", "NO", "2", "0"])
        out = []
        LibraryCLI(self.db, input_fn=lambda _: next(inputs), output_fn=out.append).run()
        self.assertIn("Deletion cancelled", out)
        self.assertIn("My Book", "\n".join(out))

    def test_invalid_input_is_handled(self):
        inputs = iter(["wrong", "1", "Book", "Author", "9781234567890",
                       "", "not-a-number", "0"])
        out = []
        LibraryCLI(self.db, input_fn=lambda _: next(inputs), output_fn=out.append).run()
        self.assertIn("Invalid option", out)
        self.assertIn("Error: Please enter a valid number", out)


if __name__ == "__main__":
    unittest.main()

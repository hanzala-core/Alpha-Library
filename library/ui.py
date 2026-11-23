"""Minimal interactive command-line user interface."""
from library import catalog, dashboard, members, loans


def render_table(headers, rows):
    rows = [tuple(str(value) for value in row) for row in rows]
    widths = [max([len(str(h))] + [len(row[i]) for row in rows])
              for i, h in enumerate(headers)]
    line = " | ".join(str(h).ljust(widths[i]) for i, h in enumerate(headers))
    bar = "-+-".join("-" * width for width in widths)
    return "\n".join([line, bar] + [
        " | ".join(row[i].ljust(widths[i]) for i in range(len(headers)))
        for row in rows
    ])


class LibraryCLI:
    def __init__(self, conn, input_fn=input, output_fn=print):
        self.conn = conn
        self.input = input_fn
        self.output = output_fn

    def prompt(self, question):
        return self.input(question).strip()

    def number(self, question):
        try:
            return int(self.prompt(question))
        except ValueError as exc:
            raise ValueError("Please enter a valid number") from exc

    def ui_add_book(self):
        title = self.prompt("Title: ")
        author = self.prompt("Author: ")
        isbn = self.prompt("ISBN: ")
        category = self.prompt("Category (blank = General): ")
        copies = self.number("Total copies: ")
        book_id = catalog.add_book(self.conn, title, author, isbn, category, copies)
        self.output(f"Added book #{book_id}")

    def ui_list_books(self):
        rows = catalog.book_rows(self.conn)
        self.output(render_table(catalog.BOOK_HEADERS, rows) if rows else "No books found")

    def ui_edit_book(self):
        book_id = self.number("Book ID to edit: ")
        old = catalog.get_book(self.conn, book_id)
        self.output("Press Enter to retain an existing field.")
        new = {}
        for field, label in [
            ("title", "Title"), ("author", "Author"),
            ("isbn", "ISBN"), ("category", "Category"),
        ]:
            val = self.prompt(f'{label} [{old[field]}]: ')
            if val:
                new[field] = val
        copies = self.prompt(f'Total copies [{old["total_copies"]}]: ')
        if copies:
            new["copies"] = copies
        catalog.edit_book(self.conn, book_id, **new)
        self.output("Book updated")

    def ui_delete_book(self):
        book_id = self.number("Book ID to delete: ")
        book = catalog.get_book(self.conn, book_id)
        confirm = self.prompt(f'Delete "{book["title"]}"? Type YES: ') == "YES"
        if not confirm:
            self.output("Deletion cancelled")
            return
        catalog.delete_book(self.conn, book_id, confirm=True)
        self.output("Book deleted")

    def ui_search_books(self):
        term = self.prompt("Search title/author/ISBN/category: ")
        rows = catalog.search_books(self.conn, term)
        if not rows:
            self.output("No books found")
            return
        self.output(render_table(
            catalog.BOOK_HEADERS,
            [(b["id"], b["title"], b["author"], b["isbn"], b["category"],
              f'{b["available"]} / {b["total_copies"]}') for b in rows],
        ))

    def ui_register_member(self):
        mid = members.register_member(
            self.conn, self.prompt("Member name: "), self.prompt("Member email: ")
        )
        self.output(f"Registered member #{mid}")

    def ui_list_members(self):
        rows = members.list_members(self.conn)
        self.output(
            render_table(("ID", "Name", "Email", "Active Loans"),
                         [(m["id"], m["name"], m["email"], m["active_loans"]) for m in rows])
            if rows else "No members found"
        )

    def ui_remove_member(self):
        member_id = self.number("Member ID to remove: ")
        if self.prompt("Type YES to confirm removal: ") != "YES":
            self.output("Removal cancelled")
            return
        members.remove_member(self.conn, member_id, confirm=True)
        self.output("Member removed")

    def ui_issue_book(self):
        book_id = self.number("Book ID: ")
        member_id = self.number("Member ID: ")
        loan_id = loans.issue_book(self.conn, book_id, member_id)
        loan = next(item for item in loans.list_active_loans(self.conn) if item["id"] == loan_id)
        self.output(f'Book issued, loan #{loan_id}; due {loan["due_date"]}')

    def ui_return_book(self):
        loan_id = self.number("Loan ID: ")
        result = loans.return_book(self.conn, loan_id)
        self.output("Book returned")
        if result["fine"]:
            self.output(f'Late by {result["days_late"]} days; fine: Rs {result["fine"]}')
        else:
            self.output("No fine due")

    def ui_list_loans(self):
        include_returned = self.prompt("Include returned loans? (y/N): ").lower() in ("y", "yes")
        rows = loans.list_loans(self.conn, include_returned=include_returned)
        if not rows:
            self.output("No loans found" if include_returned else "No active loans")
            return
        self.output(render_table(
            ("Loan ID", "Title", "Member", "Issued", "Due", "Status", "Days late", "Fine (Rs)"),
            [(l["id"], l["title"], l["member"], l["issued_at"], l["due_date"],
              l["status"], l["days_late"], l["fine"]) for l in rows],
        ))

    def ui_dashboard(self):
        data = dashboard.dashboard_data(self.conn)
        self.output(
            "\n=== LIBRARY DASHBOARD ===\n"
            f'Book titles: {data["book_titles"]}\n'
            f'Registered members: {data["registered_members"]}\n'
            f'Active loans: {data["active_loans"]}\n'
            f'Overdue loans: {data["overdue_loans"]}'
        )
        if data["overdue_list"]:
            self.output(render_table(
                ("Loan ID", "Title", "Member", "Due", "Days late", "Fine (Rs)"),
                [(l["id"], l["title"], l["member"], l["due_date"],
                  l["days_late"], l["fine"]) for l in data["overdue_list"]],
            ))
        else:
            self.output("No overdue loans")

    def ui_reset_sample_data(self):
        if self.prompt("This replaces ALL library data with demo data. Type RESET to confirm: ") != "RESET":
            self.output("Sample-data reset cancelled")
            return
        dashboard.reset_sample_data(self.conn, confirm=True)
        self.output("Sample data restored; all previous books, members, and loans were replaced.")

    def run(self):
        actions = {
            "1": self.ui_add_book, "2": self.ui_list_books, "3": self.ui_edit_book,
            "4": self.ui_delete_book, "5": self.ui_search_books,
            "6": self.ui_register_member, "7": self.ui_list_members,
            "8": self.ui_remove_member, "9": self.ui_issue_book,
            "10": self.ui_return_book, "11": self.ui_list_loans,
            "12": self.ui_dashboard, "13": self.ui_reset_sample_data,
        }
        while True:
            self.output(
                "\n=== ALPHA LIBRARY ===\n"
                "1 Add book | 2 List books | 3 Edit book | 4 Delete book\n"
                "5 Search books | 6 Register member | 7 List members\n"
                "8 Remove member | 9 Issue book | 10 Return book\n"
                "11 Loans (active/returned) | 12 Dashboard | 13 Reset sample data | 0 Exit"
            )
            try:
                choice = self.prompt("Choose option: ")
            except (KeyboardInterrupt, EOFError):
                self.output("\nGoodbye")
                return
            if choice == "0":
                self.output("Goodbye")
                return
            if choice not in actions:
                self.output("Invalid option")
                continue
            try:
                actions[choice]()
            except ValueError as exc:
                self.output(f"Error: {exc}")

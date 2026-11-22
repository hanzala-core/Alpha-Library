# Alpha Library - Test Case Specification

Unit tests are maintained in \`tests/\`. The expected command is:

\`\`\`bash
python -m unittest discover -s tests -v
\`\`\`

Do not report passing tests until a real local or GitHub Actions run confirms them.

| Scenario | Expected outcome | Relevant test |
|---|---|---|
| Valid book add | ID generated; ISBN normalized | test_add_book_and_normalize_isbn |
| Invalid ISBN / missing title | ValueError; no insertion | test_invalid_isbn, test_required_fields_and_positive_copies |
| Duplicate ISBN | Rejected | test_duplicate_normalized_isbn |
| Book listing | Sorted by title, correct availability | test_sorting_and_book_rows, test_available_counts_and_return |
| Edit book | Details updated; loan constraint enforced | test_edit_book, test_edit_cannot_reduce_copies_below_active_loans |
| Delete book on loan | Rejected | test_delete_blocked_with_active_loan |
| Search | All fields, case-insensitive | test_search_all_fields_case_insensitive |
| Member registration | Valid email accepted; duplicates rejected | test_register_member, test_duplicate_email_case_insensitive |
| Member removal with active loan | Rejected | test_cannot_remove_with_active_loans |
| Borrow/return | Availability updated correctly | test_issue_book, test_return_book |
| CLI input | Errors handled and menu continues | test_invalid_input_is_handled |

## Review evidence
Capture the actual unit-test output and application demonstrations after code review; screenshots of planned data alone do not count as execution evidence.

# Alpha Library - Test Case Specification

Run the complete regression suite with:

```bash
python -m unittest discover -s tests -v
```

| Requirement | Expected outcome | Automated coverage |
|---|---|---|
| Existing book catalogue and validation | ISBN normalized/validated; CRUD constraints preserved | `tests/test_catalog.py` |
| US-06: loan term | Due date is exactly 14 calendar days after issue | `test_issue_due_exactly_fourteen_days` |
| US-06: member loan limit | Three active loans succeed; a fourth fails; returned loan no longer counts | `test_member_maximum_three_active_loans_boundary`, `test_returned_loan_does_not_count_toward_three_limit` |
| US-06: duplicate and availability checks | Same member cannot borrow the same title twice while active; no available copy fails without changing counts | `test_duplicate_active_same_book_member_rejected_even_with_copies`, `test_cannot_issue_when_no_copies_available` |
| US-07: loan ID return | Return identifies an active loan by ID, restores one available copy, and rejects duplicate returns | `test_return_by_loan_id_restores_availability_and_prevents_duplicate` |
| US-07: history listing | Default returns active only; explicit option includes returned loans | `test_list_defaults_to_active_and_can_include_returned` |
| US-08: date boundaries | Before/on due date has zero late days; first late day is overdue | `test_days_late_and_fine_boundaries` |
| US-08: fines | Rs 10 per late day; returned late loans retain final days and fine | `test_return_late_calculates_final_fine` |
| US-08: loan reporting | Active listing exposes overdue status, days late, and accrued fine | `test_active_loan_listing_shows_overdue_days_and_fine` |
| US-09: dashboard totals | Active titles, members, loans, overdue count and overdue detail are accurate | `tests/test_dashboard.py` |
| US-09: sample reset | Requires explicit confirmation; confirmed reset restores demo fixtures | `test_reset_requires_explicit_confirmation_and_preserves_without_call`, `test_confirmed_reset_replaces_records_with_sample_fixture` |
| CLI integration | Dashboard, confirmation prompts and existing menu flows work | `tests/test_ui.py` |
| SQLite upgrade | Existing loans receive derived due dates without deleting records | Existing database migration code in `library/database.py` |

Date-sensitive behavior is tested with fixed ISO dates, so the test suite does not depend on the machine's current date.

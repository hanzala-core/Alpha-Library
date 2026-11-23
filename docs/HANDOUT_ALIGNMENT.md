# Alignment with Miss Mahnoor's Actual Scrum Handout (Labs 9–11)

**Primary source:** `scrum.pdf`, *Scrum with GitHub Projects — Library Management System Lab Activity*, 37 pages. This handout supersedes the older generic ASP.NET workbook instructions **for this specific assigned Scrum activity**.

## The key outcome

The lab's purpose is to practise Scrum using GitHub Projects. Appendix A provides a complete **offline Python** library program. Developers are instructed to introduce **only their assigned story's portion of the appendix code on individual feature branches** and integrate it after human reviews. The team should not assume it must finish all 9 stories in two short sprints.

## Correct people and responsibilities
- **Product Owner:** @Dev-Rayyan-Ahmed — sets Product Goal, writes and orders user stories, accepts/rejects increments. Handout says PO does not write code during the sprint.
- **Scrum Master:** @hanzala-core — board, fields, workflow automation, sprint events, Scrum Log, blockers, quality of process. May do only a small development task when the sprint is at risk.
- **Developers:** @AnasMalick887 and @chotimau — estimation, child tasks, feature branches, code, tests and cross-reviews.
- **Stakeholder:** Miss Mahnoor (instructor) — feedback and change request after Sprint 1.

US-01 (#2) and its four coding subtasks have been **provisionally reassigned to Anas** from the PO account, because the handout says the PO does not code. Team confirmation remains required.

## Required Product Backlog: Nine stories

| Story | Priority given in handout | User outcome | Current repository |
|---|---|---|---|
| US-01 | Must | Add a book, validated unique ISBN | #2 exists |
| US-02 | Must | List catalogue with available / total | #3 exists |
| US-03 | Should | Edit/delete with active-loan constraints | #4 exists |
| US-04 | Should | Search title, author, ISBN, category | #15 exists |
| US-05 | Must | Register/remove members safely | #17 exists |
| US-06 | Must | Issue a book: available copy, 14-day due date, max 3 active loans per member, avoid duplicate copy | [#26](https://github.com/hanzala-core/Alpha-Library/issues/26) — drafted by SM, awaiting PO approval |
| US-07 | Must | Return a book by loan ID, update availability, active/returned loan listing | [#27](https://github.com/hanzala-core/Alpha-Library/issues/27) — drafted by SM, awaiting PO approval |
| US-08 | Should | Overdue loans and Rs 10 per day fines | [#28](https://github.com/hanzala-core/Alpha-Library/issues/28) — drafted by SM, awaiting PO approval |
| US-09 | Could | Dashboard: book titles, members, loans, overdue, reset sample data | [#29](https://github.com/hanzala-core/Alpha-Library/issues/29) — drafted by SM, awaiting PO approval |

The Developers agree the size with **planning poker**; do not fabricate an estimation meeting. L-sized stories must be split before entering a sprint.

## Correct sprint selection (example; team/PO must agree)
**Sprint 1 proposed:** [skeleton #30](https://github.com/hanzala-core/Alpha-Library/issues/30) + US-01 (M) + US-02 (S). Sprint Goal: a librarian can add books and see the catalogue.

**Sprint 2 proposed:** another realistic combination based on Sprint 1 feedback, e.g. US-05 (M) or US-04 (S). Do **not** predeclare US-03, US-04 and US-05 as committed or Done. The handout estimates roughly one M and one S for each short Sprint.

## Required GitHub Projects setup by Scrum Master

- Project name: **Alpha Library Scrum Board** (linked to repository); add team members.
- **Status** options (exactly five): Product Backlog → Sprint Backlog → In Progress → In Review → Done.
- **Size** single select: S / M / L.
- **Priority** single select: Must / Should / Could.
- **Sprint** iteration field: Sprint 1 / Sprint 2.
- **Product Backlog** table view: Title, Priority, Size, Status, grouped by Priority, not sorted.
- **Sprint Board** board view: grouped by Status, filter `sprint:@current`.
- Workflows: **Auto-add issues**; new items → Product Backlog; issue closed and PR merged → Done.
- Main branch protection: pull request and at least one approval.
- Scrum Log #1 pinned (and archived from board if included).
- Sprint 1 and 2 **status charts** in Insights with real data, screenshotted and posted to Scrum Log.

**Actual status:** Board, views, fields, workflow settings, protected branch and Insights evidence are not confirmed completed. Track them in [SM issue #31](https://github.com/hanzala-core/Alpha-Library/issues/31).

## Process evidence: Nine phases from handout

1. Team formation (5 min) — roles recorded in README.
2. Repository + board (15 min) — public repo, collaborators, README/DoD, labels, template, project fields and automations.
3. Product backlog (15 min) — nine user-story issues, PO ordering, Developer sizing.
4. Sprint 1 Planning (10 min) — Goal, realistic capacity, story sub-issues (including skeleton).
5. Sprint 1 Work (35 min) — real Developer branches, commits, individual PRs, cross-review, 5-min Daily Scrum recorded by SM.
6. Sprint 1 Review (10 min) — demo latest main, PO checks acceptance, Stakeholder feedback, Sprint 1 status chart.
7. Sprint 1 Retrospective (5 min) — real comments from each member and improvements.
8. Backlog refinement (5 min) — actual instructor change request written by PO, resized/reordered.
9. Sprint 2 (50 min) — plan, work, Daily Scrum, review, retrospective, chart, velocity and PO release `v1.0` on main describing delivered stories.

**No invented meeting comments, teacher feedback, contributor approvals, or sprint dates.**

## Definition of Done (applies to each actually delivered story)
- Every acceptance criterion is met.
- Code lives on a feature branch and is merged to main through a PR.
- The **other Developer** reviewed and approved PR.
- PR closes its own issue using `Closes #...`.
- `python main.py` runs and `python -m unittest` passes.
- The Product Owner accepted the story at a real Sprint Review.

## Appendix A compatibility gap vs the proposed integration prototype (PR #25)

| Handout Appendix A | PR #25 implementation |
|---|---|
| Python 3.10+; `storage.py` with `library_data.json`, sample data | Python 3.11+; SQLite `library/database.py`, local DB |
| `books.py`, `members.py`, `loans.py`, `dashboard.py` | `library/catalog.py`, `library/members.py`, `library/loans.py`; dashboard missing |
| `test_library.py`, `python -m unittest -v` | 36 tests across `tests/`; `python -m unittest discover -s tests -v` |
| Due dates + max 3 loans + same-copy restriction | Not yet implemented |
| Rs 10/day overdue/fine functions | Not yet implemented |
| Dashboard and sample-data reset | Not yet implemented |
| Story-by-story feature PRs from two Developers | One Scrum Master-authored integration prototype PR, pending team review |

Passing 36 tests in PR #25 demonstrates quality of **that implementation's current scope**, not full Appendix A or Scrum lab compliance. Do not merge it claiming exact teacher handout execution. Plan as a reference/demo only unless the real team agrees to adjust it.

## Next steps and owners

1. **PO Rayyan:** review and approve SM-drafted US-06 to US-09 (#26–#29), confirm all nine story priorities, obtain teacher's real change request, and approve actual Sprint Goals and completed work. Keep existing issue history.
2. **Developers Anas/Faiz:** agree estimates, select story tasks; implement and review through **their own accounts**, using Appendix A story-scoped code as instructed.
3. **SM Hanzala:** configure the GitHub Project and protection settings in UI, organize real sprint evidence in Scrum Log, capture genuine Insights charts; make sure sprint capacity/DoD are honest.
4. **Team:** run real application and tests, record actual review/retro and PO acceptance. Only then close eligible stories, mark Done and consider release.

This document is a **source-based gap checklist**; it is not evidence that the incomplete actions happened.

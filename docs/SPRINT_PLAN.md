# Alpha Library - Scrum Sprint Plan (Miss Mahnoor handout)

**Authoritative reference:** the 37-page `scrum.pdf`, *Scrum with GitHub Projects — Library Management System Lab Activity*. See [Detailed Handout Alignment](HANDOUT_ALIGNMENT.md) for the nine-phase checklist and actual-vs-required gap.

**Planning note:** This is the Scrum Master's **proposal**, not a substitute for the Product Owner's ordering or actual Developer planning-poker estimates. Sprint dates, capacity, acceptance and review outcomes must be recorded from real team events.

## Team and Scrum accountabilities

| Role | Account | Assignment |
|---|---|---|
| Product Owner | @Dev-Rayyan-Ahmed | Owns Product Backlog ordering, answers questions, obtains stakeholder feedback, accepts/rejects stories. Does not code during sprint. |
| Scrum Master | @hanzala-core | Configures project, runs events, removes blockers, records Scrum Log and Insights screenshots; may help with one small coding task only if sprint at risk. |
| Developer | @AnasMalick887 | Estimates and delivers selected tasks on feature branches; reviews the other Developer's PRs. |
| Developer | @chotimau | Estimates and delivers selected tasks on feature branches; reviews the other Developer's PRs. |
| Stakeholder | Miss Mahnoor | Requirements, Sprint Review feedback and post-Sprint-1 change request. |

## Product Goal

A simple system for a department library to keep track of books, registered members and borrowing activity.

## All nine product-backlog user stories

| Story | Handout priority | Repo link or next action |
|---|---|---|
| US-01 Add book | Must | [Issue #2](https://github.com/hanzala-core/Alpha-Library/issues/2) |
| US-02 List books | Must | [Issue #3](https://github.com/hanzala-core/Alpha-Library/issues/3) |
| US-03 Edit/delete books | Should | [Issue #4](https://github.com/hanzala-core/Alpha-Library/issues/4) |
| US-04 Search catalogue | Should | [Issue #15](https://github.com/hanzala-core/Alpha-Library/issues/15) |
| US-05 Member registration/removal | Must | [Issue #17](https://github.com/hanzala-core/Alpha-Library/issues/17) |
| US-06 Issue a book | Must | [Issue #26](https://github.com/hanzala-core/Alpha-Library/issues/26) — PO to approve and prioritise |
| US-07 Return a book | Must | [Issue #27](https://github.com/hanzala-core/Alpha-Library/issues/27) — PO to approve and prioritise |
| US-08 Overdue loans/fines | Should | [Issue #28](https://github.com/hanzala-core/Alpha-Library/issues/28) — PO to approve and prioritise |
| US-09 Dashboard | Could | [Issue #29](https://github.com/hanzala-core/Alpha-Library/issues/29) — PO to approve and prioritise |

The backlog may exceed sprint capacity **on purpose**. The PO orders it; Developers estimate S/M/L with planning poker. Split any L item before committing it to a Sprint.

## Sprint 1 - Proposed initial commitment

**Proposed Sprint Goal:** A librarian can add books and see the complete catalogue.

**Example commitment from teacher handout:** 
- Shared Appendix A application skeleton — [Task #30](https://github.com/hanzala-core/Alpha-Library/issues/30), proposed Faiz
- **US-01 Add book (reference M)** — proposed Anas (handout says PO should not code)
- **US-02 List books (reference S)** — proposed Faiz

Use 35-minute implementation timebox after 10 minutes planning. Developers break only selected stories into sub-issues, work on their own branches, request human PR review and add tests in the same PR. At the real Daily Scrum, the SM records what each Developer finished, their next plan and blockers as a comment on [Scrum Log #1](https://github.com/hanzala-core/Alpha-Library/issues/1).

**Sprint Review:** The PO checks actual acceptance criteria; the instructor's feedback is noted; only accepted stories meeting DoD become Done. Create an Insights **Sprint 1 status** chart and attach a real screenshot to Scrum Log.

**Retrospective:** Each member provides actual observations; the SM records the improvement issue(s). The instructor's actual change request is added by the PO during backlog refinement.

## Sprint 2 - Select at the next planning meeting

**Possible selection:** US-05 (reference M), or US-04 (reference S), or another combination that fits actual capacity. Carry over unfinished work only if the PO still prioritises it.

The second Sprint has planning (5 minutes), work (30 minutes), Daily Scrum, Review (10 minutes), Retrospective (5 minutes). Repeat actual branch/PR/review/test/PO acceptance evidence and create **Sprint 2 status** chart.

Afterward compare real velocity (finished story counts and sizes) and log it. The PO creates `v1.0` release on main listing genuinely delivered stories.

## Definition of Done

1. Every acceptance criterion met.
2. Code merged to `main` from a feature branch through a PR.
3. The other Developer reviewed and approved.
4. PR closes its own issue with `Closes #...`.
5. `python main.py` runs and `python -m unittest` passes.
6. PO accepted the story during Sprint Review.

## GitHub Projects settings required

Track real configuration in [SM Task #31](https://github.com/hanzala-core/Alpha-Library/issues/31). Neither project creation nor Sprint commitment is verified by this document.

Project **Alpha Library Scrum Board** with:
- Status: **Product Backlog / Sprint Backlog / In Progress / In Review / Done**
- Priority: Must / Should / Could
- Size: S / M / L
- Sprint: Sprint 1 / Sprint 2
- Views: Product Backlog (table grouped by Priority, unsorted) and Sprint Board (board by Status, filtered `sprint:@current`)
- Workflows: auto-add issues; new → Product Backlog; closed issue and merged PR → Done
- Main branch protection: 1 PR approval required
- Sprint status Insights charts with screenshots

For status and screenshot checks see [Evidence Checklist](EVIDENCE_CHECKLIST.md). No project board/field/automation is marked complete simply because it appears in these documents.

## Reference-code mismatch

Appendix A uses **Python 3.10+, JSON sample data, `storage.py`, `books.py`, `members.py`, `loans.py`, `dashboard.py` and `test_library.py`**. Existing separate integration PR #25 contains a SQLite CLI application and 43 passing tests covering US-01 through US-09 core behaviors (including loan due dates, member loan limit, fines, and dashboard). Its implementation architecture remains different from Appendix A. Its 43 passing tests are valid for that prototype, **not proof of strict Appendix A compliance or genuine story-by-story Scrum delivery**. Preserve PR #25 pending an explicit team decision; do not merge it as if it completed the handout steps.

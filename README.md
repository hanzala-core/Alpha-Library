# Alpha Library

**Collaborative Library Management System** managed using Scrum, GitHub Issues and pull requests.

> **Current status:** Nine user stories and technical task backlog prepared; Product Owner approval and GitHub Projects board still pending. A separate **SQLite integration prototype** is available in [PR #25](https://github.com/hanzala-core/Alpha-Library/pull/25), with 43 passing unit tests, but is not merged or accepted as a Scrum Increment.

## Team and responsibilities

| Scrum role | Member | GitHub |
|---|---|---|
| Scrum Master | Muhammad Hanzala | [@hanzala-core](https://github.com/hanzala-core) |
| Product Owner | Rayyan Ahmed | [@Dev-Rayyan-Ahmed](https://github.com/Dev-Rayyan-Ahmed) |
| Developer | Anas Malick | [@AnasMalick887](https://github.com/AnasMalick887) |
| Developer | Muhammad Faiz | [@chotimau](https://github.com/chotimau) |
| Stakeholder | Miss Mahnoor | Instructor |

The Scrum Master coordinates planning and removes blockers. The Product Owner prioritizes and accepts stories. Developers implement and review code. Assignments are visible in the issues.

## Product goal

Build a small library catalogue and member-management system. A planned Python command-line application will support book catalogue actions and library member records. No application code has been merged yet.

## Product backlog

The nine instructor-specified user stories are open and waiting for actual PO approval, Developer estimates and realistic Sprint selection. **The Sprint column below does not imply commitment.**

| Story | Handout priority | Proposed owner / reviewer |
|---|---|---|
| [US-01 Add book #2](https://github.com/hanzala-core/Alpha-Library/issues/2) | Must | Anas — proposed Developer for Sprint 1 |
| [US-02 List books #3](https://github.com/hanzala-core/Alpha-Library/issues/3) | Must | Faiz — proposed Developer for Sprint 1 |
| [US-03 Edit/delete book #4](https://github.com/hanzala-core/Alpha-Library/issues/4) | Should | Anas — backlog |
| [US-04 Search books #15](https://github.com/hanzala-core/Alpha-Library/issues/15) | Should | Anas — backlog |
| [US-05 Manage members #17](https://github.com/hanzala-core/Alpha-Library/issues/17) | Must | Faiz — backlog |
| [US-06 Issue book #26](https://github.com/hanzala-core/Alpha-Library/issues/26) | Must | Rayyan to review/prioritize |
| [US-07 Return book #27](https://github.com/hanzala-core/Alpha-Library/issues/27) | Must | Rayyan to review/prioritize |
| [US-08 Overdue/fines #28](https://github.com/hanzala-core/Alpha-Library/issues/28) | Should | Rayyan to review/prioritize |
| [US-09 Dashboard #29](https://github.com/hanzala-core/Alpha-Library/issues/29) | Could | Rayyan to review/prioritize |

**Scrum Master setup:** [GitHub Projects board #31](https://github.com/hanzala-core/Alpha-Library/issues/31). **Sprint 1 skeleton:** [Task #30](https://github.com/hanzala-core/Alpha-Library/issues/30). Actual team review and planning-poker estimates still required.

See the [handout-alignment checklist](docs/HANDOUT_ALIGNMENT.md), [Sprint Plan](docs/SPRINT_PLAN.md) and [Scrum Log #1](https://github.com/hanzala-core/Alpha-Library/issues/1).

## Development workflow

1. Start work from an assigned GitHub issue and agree its acceptance criteria.
2. Create a feature branch from current `main` (e.g. `feat/us-02-list-books`).
3. Implement the smallest task, write and run its tests, and commit.
4. Open a pull request targeting `main`; reference the issue in its body (`Closes #123` only when fully finished).
5. Request a review from another team member, address feedback, and merge only when accepted.
6. Update the issue / GitHub Projects board and link the actual proof in the sprint review.

## Definition of Done

- [ ] All story acceptance criteria are met.
- [ ] Feature is committed on a branch and merged through a reviewed pull request.
- [ ] Appropriate tests pass and actual output can be demonstrated.
- [ ] Related issue is closed by the merged work.
- [ ] Product Owner accepts the story during sprint review.

**Teacher handout's intended verification:** `python main.py` and `python -m unittest` after story-scoped code is reviewed and merged to `main`. PR #25 separately reports 43 passing tests on its own branch; this does not demonstrate approved Sprint completion.

## Documentation

- [Sprint plan and team backlog](docs/SPRINT_PLAN.md)
- [Evidence and submission checklist](docs/EVIDENCE_CHECKLIST.md)
- [Scrum Log](https://github.com/hanzala-core/Alpha-Library/issues/1)

*GitHub Issues, PR history, Projects screenshots and implemented/tested code should reflect real activity, not simulated completion.*

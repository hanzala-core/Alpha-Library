# Alpha Library

**Collaborative Library Management System** managed using Scrum, GitHub Issues and pull requests.

> **Current status:** Requirements and task backlog prepared. Application implementation and test evidence are pending. Open issues are not completed features.

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

| Sprint | User story | Current assignee |
|---|---|---|
| Sprint 1 | [US-01: Add a book](https://github.com/hanzala-core/Alpha-Library/issues/2) | Rayyan |
| Sprint 1 | [US-02: List books](https://github.com/hanzala-core/Alpha-Library/issues/3) | Faiz |
| Sprint 1 | [US-03: Edit/delete book](https://github.com/hanzala-core/Alpha-Library/issues/4) | Anas |
| Sprint 2 | [US-04: Search books](https://github.com/hanzala-core/Alpha-Library/issues/15) | Anas |
| Sprint 2 | [US-05: Manage members](https://github.com/hanzala-core/Alpha-Library/issues/17) | Faiz |

See the linked story for acceptance criteria and child-task references. See [Sprint Plan](docs/SPRINT_PLAN.md) for proposed sequence and evidence requirements. Record real meeting outcomes in [Scrum Log #1](https://github.com/hanzala-core/Alpha-Library/issues/1).

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

**Planned execution (not yet verified):** `python main.py` and `python -m unittest`, once implementation and tests are committed.

## Documentation

- [Sprint plan and team backlog](docs/SPRINT_PLAN.md)
- [Evidence and submission checklist](docs/EVIDENCE_CHECKLIST.md)
- [Scrum Log](https://github.com/hanzala-core/Alpha-Library/issues/1)

*GitHub Issues, PR history, Projects screenshots and implemented/tested code should reflect real activity, not simulated completion.*


## Running the working integration prototype

The application code is proposed in the feature branch [\`feat/working-library-integration\`](https://github.com/hanzala-core/Alpha-Library/tree/feat/working-library-integration), associated with integration [PR #25](https://github.com/hanzala-core/Alpha-Library/pull/25).

**Prerequisites:** Python 3.11 or newer. No third-party Python packages are required.

Clone and switch to the implementation branch:

\`\`\`bash
git clone https://github.com/hanzala-core/Alpha-Library.git
cd Alpha-Library
git switch feat/working-library-integration
python main.py
\`\`\`

For a separate demonstration database:

\`\`\`bash
python main.py --db lab_demo.db
\`\`\`

The app creates the SQLite database on first run. Use the numbered menu to add/list/edit/delete books, search the catalogue, register/list/remove members, issue and return books, and review active loans. Copies are automatically calculated from outstanding loans. The file is local and ignored by Git.

Run automated regression tests:

\`\`\`bash
python -m unittest discover -s tests -v
\`\`\`

GitHub Actions also runs tests on proposed branches and pull requests.

### Implementation files
- \`main.py\`: CLI entry point, optional database path
- \`library/database.py\`: database schema and connection
- \`library/catalog.py\`: book catalogue CRUD and search
- \`library/members.py\`: library member management
- \`library/loans.py\`: issue/return operations
- \`library/ui.py\`: numbered interactive CLI
- \`tests/\`: automated regression tests
- \`docs/REQUIREMENTS.md\`: functional and non-functional requirements
- \`docs/TEST_CASES.md\`: testing specification
- \`docs/CLI_WIREFRAME.md\`: CLI wireframe (not an ASP.NET website)

**Sprint evidence status:** Creating application code and opening an integration PR does not mean the original assignees have implemented/reviewed their stories. Do not close story issues or report sprint completion until real human reviews, demonstrations and Product Owner acceptance occur.

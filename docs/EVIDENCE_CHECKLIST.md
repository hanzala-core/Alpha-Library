# CS-326 Labs 9–11 — Actual Scrum Evidence Checklist

**Primary source:** Miss Mahnoor's 37-page handout, *Scrum with GitHub Projects — Library Management System Lab Activity*. See [Handout Alignment](HANDOUT_ALIGNMENT.md). Use the other group's screenshot PDF only as a visual reference; never submit their screenshots as Alpha Library work.

Mark a checkbox only after **real Alpha Library evidence** is available.

## Phase 1: Team and roles
- [ ] Public repository page with team name, PO/SM/two Developers, instructor as Stakeholder
- [ ] Readme with accurate account names and Definition of Done
- [ ] Actual collaborator access evidence (do not publish secrets)

## Phase 2: GitHub Projects configuration (SM)
- [ ] Repository and contributor access
- [ ] Issue labels: user-story, task, bug, blocked
- [ ] .github/ISSUE_TEMPLATE/user-story.md
- [ ] Board named **Alpha Library Scrum Board** linked to repository
- [ ] Project collaborators added
- [ ] Five status choices: Product Backlog, Sprint Backlog, In Progress, In Review, Done
- [ ] Priority single select: Must, Should, Could
- [ ] Size single select: S, M, L
- [ ] Sprint iteration field: Sprint 1, Sprint 2
- [ ] Product Backlog table grouped by Priority, not sorted
- [ ] Sprint Board grouped by Status, filtered to \`sprint:@current\`
- [ ] Workflows: Auto-add issues, Item added -> Product Backlog, Item closed -> Done, PR merged -> Done
- [ ] Main branch protection, require a PR and one approval
- [ ] Pin Scrum Log #1; archive from backlog board if auto-added

## Phase 3: Product Backlog (PO + Developers)
- [ ] PO created/confirmed all nine user stories US-01..US-09 (currently US-06..US-09 absent)
- [ ] Each story has testable checkbox acceptance criteria, user-story label and handout priority
- [ ] Product Owner ordered backlog items
- [ ] Developers genuinely estimated using S/M/L planning poker; SM records agreed Size
- [ ] Larger-than-capacity (L) stories split into smaller stories before entering Sprint

## Phase 4: Sprint 1 Planning
- [ ] Agreed Sprint Goal recorded in iteration description and Scrum Log
- [ ] Realistic capacity; teacher's example = skeleton + US-01 (M) + US-02 (S)
- [ ] Selected stories moved to Sprint Backlog, assigned to Sprint 1
- [ ] Technical tasks recorded as actual sub-issues with task label and Developer assignees
- [ ] Skeleton task tracked, with starter files per Appendix A

## Phase 5: Sprint 1 Work and Daily Scrum
- [ ] Separate real Developer branch, commits, linked issues and PRs
- [ ] Other Developer's actual PR review comment AND approval
- [ ] Automated tests and \`python main.py\` evidence for only completed stories
- [ ] Cards accurately move In Progress -> In Review -> Done after acceptance
- [ ] Actual 5-minute Daily Scrum answers as one dated comment in Scrum Log
- [ ] Blocker label and PO escalation where actually needed

## Phase 6: Sprint 1 Review
- [ ] Demonstrate merged Increment from current main, not a detached prototype branch
- [ ] Actual PO acceptance/rejection against criteria, recorded truthfully
- [ ] Actual instructor/stakeholder feedback if received
- [ ] **Sprint 1 status chart** in GitHub Projects Insights; attach real screenshot to Scrum Log
- [ ] Rejected/unfinished work appropriately returned/carry-over noted

## Phase 7: Sprint 1 Retrospective
- [ ] Sprint 1 Retrospective issue with headings: What went well / What did not go well / What we will change
- [ ] Real comments from all group members
- [ ] One or two agreed improvements with owner/issues for next Sprint

## Phase 8: Change Request and Refinement
- [ ] Instructor's actual change request obtained (do not invent)
- [ ] Product Owner wrote it as a user story, prioritised it and Developers sized it
- [ ] Actual change in backlog order documented

## Phase 9: Sprint 2
- [ ] Sprint 2 Goal, team size estimates, realistic selection and actual sub-issues
- [ ] Feature branches, unit tests, two-way PR reviews and actual merge(s)
- [ ] Actual 5-minute Daily Scrum and real Sprint Review/Retrospective records
- [ ] **Sprint 2 status chart** in GitHub Projects Insights, with screenshot in Scrum Log
- [ ] Team velocity compared by counts and sizes of accepted stories in each Sprint
- [ ] Product Owner release \`v1.0\` on main listing only accepted delivered stories

## Application / Appendix A compatibility
- [ ] Team agrees whether to use handout's JSON-based Appendix A code or a reviewed variation
- [ ] If claiming US-06: 14-day due date, no duplicate copy, max 3 concurrent loans tested
- [ ] If claiming US-08: overdue list and Rs 10/day late fine tested
- [ ] If claiming US-09: dashboard and reset sample data tested
- [ ] Real \`python main.py\` run output
- [ ] Real \`python -m unittest\` successful tests for accepted stories

**Important:** Existing PR #25 contains a separate SQLite prototype with 43 passing tests. That fact alone does NOT demonstrate the handout's sprint-by-sprint process, Appendix A compatibility, instructor change request, board configuration or PO approval.

# Scrum Sprint Plan - Alpha Library

**Planning status:** proposed; no sprint is declared completed. Validate scope and assignments with the Product Owner before execution.

## Product vision
A small library catalogue with basic book and member management. User stories are tracked in GitHub Issues. Feature branches and pull requests record code contributions, reviews and integration.

## Team
- Product Owner: @Dev-Rayyan-Ahmed - prioritization, acceptance, stakeholder communication
- Scrum Master: @hanzala-core - facilitate planning, standups, blockers, review and retrospective
- Developer: @AnasMalick887 - edit/delete books and search, testing and peer review
- Developer: @chotimau - list books and member management, testing and peer review

The existing issue history assigns Add Book to the Product Owner account. This is preserved, but code ownership can be delegated by the team during sprint planning.

## Sprint 1 - Core catalogue
**Goal:** enable essential librarian actions on catalogue records.

| Story | Tasks | Responsible account |
|---|---|---|
| [US-01 Add Book #2](https://github.com/hanzala-core/Alpha-Library/issues/2) | #11 #13 #14 #16 | @Dev-Rayyan-Ahmed |
| [US-02 List Books #3](https://github.com/hanzala-core/Alpha-Library/issues/3) | #5 #6 #7 | @chotimau |
| [US-03 Edit/Delete #4](https://github.com/hanzala-core/Alpha-Library/issues/4) | #8 #9 #10 #12 | @AnasMalick887 |

**Sprint review evidence (only after implementation):** running app, book add/list/edit/delete demonstrations, rejection cases, automated tests, feature branches, peer-reviewed PRs. Record results and blockers in #1.

## Sprint 2 - Discovery, members and integration
**Goal:** deliver searchable catalogue and member registration/removal, then verify integrated flows.

| Story | Tasks | Responsible account |
|---|---|---|
| [US-04 Search #15](https://github.com/hanzala-core/Alpha-Library/issues/15) | #18 #19 #20 | @AnasMalick887 |
| [US-05 Members #17](https://github.com/hanzala-core/Alpha-Library/issues/17) | #21 #22 #23 | @chotimau |

**Sprint review evidence (only after implementation):** search tests, member validation, blocked removal with loans, integration tests, code reviews, final CLI demonstration and PO sign-off.

## Scrum working agreement
- Product backlog: open, prioritized user stories with acceptance criteria.
- Sprint backlog: stories committed for a sprint, broken into tasks assigned to collaborators.
- Daily scrum: what was done, what is next, blockers; record actual notes as comments in [Scrum Log #1](https://github.com/hanzala-core/Alpha-Library/issues/1).
- Sprint review: demonstrate working code and record PO feedback; do not mark an issue Done based on a plan.
- Retrospective: list one improvement action and owner after each real review.
- PR workflow: new branch -> commit -> PR to main -> other contributor reviews -> tests pass -> merge -> close issue.

## Suggested GitHub Projects board
Create or link a GitHub Project for this repository with status columns:
**Product Backlog** -> **Sprint Backlog** -> **In Review** -> **Done**.
Add custom fields: **Priority** (Must/Should/Could), **Size** (S/M/L) and **Sprint** (Sprint 1/Sprint 2). The board, fields, workflows and insights must be configured and captured in GitHub itself; this document does not imply they already exist.

## Suggested planning priority
- **Must:** US-01, US-02, US-03
- **Should:** US-04, US-05
- **Could:** dashboard or other improvements, only after core acceptance

## Source alignment
The team's supplied screenshot PDF shows another group's GitHub Projects approach (user stories, backlog, status, priority, size, sprint fields and insights). This file is the Alpha Library team's proposed adaptation, not evidence that those views have already been created.

The original workbook also describes ASP.NET web pages and wireframes; a Python CLI workflow by itself should not be represented as having fulfilled those web-page exercises unless the instructor approved the adapted Scrum activity.

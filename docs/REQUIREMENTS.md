# Alpha Library - Requirement Specification (proposed)

## Purpose
Implement a small library catalogue and member-management system, guided by five approved-as-planned user stories in GitHub Issues. The code exists on the integration feature branch until reviewed and merged.

## Actors
- **Librarian**: add, list, edit, delete, search, issue and return books.
- **Administrator**: register and remove members.
- **Member**: represented by the borrower's account; member-facing self-service login is outside current scope.
- **Scrum Team**: owns review and delivery of user stories.

## Functional requirements
| ID | Requirement | Story |
|---|---|---|
| FR-01 | Add book with required title, author, unique 10/13-digit ISBN and copies >=1 | #2 |
| FR-02 | List all books by title with available/total counts | #3 |
| FR-03 | Edit and delete books, preventing deletion while on loan | #4 |
| FR-04 | Search title, author, ISBN or category without case sensitivity | #15 |
| FR-05 | Register members with unique valid email; prevent removal on active loan | #17 |
| FR-06 | Issue books if copies exist and member is registered | Supporting workflow |
| FR-07 | Return loans and restore availability | Supporting workflow |
| FR-08 | Persist data between runs using SQLite | Supporting workflow |

## Non-functional requirements
- **Usability**: numbered menu, readable errors, no external dependencies.
- **Reliability**: input validation, transactions, referential integrity and tests.
- **Maintainability**: separate catalogue, members, loans, database and UI modules.
- **Portability**: Python 3.11+ on Windows, Linux or macOS.
- **Security**: SQL parameter binding; email validation; no hard-coded secrets.
- **Data retention**: returned loans are kept in history. To prevent deleting historical records, the application also refuses deletion of books/members referenced by completed loans.

## Scope note for the lab workbook
This existing Scrum team's implementation target is a **Python command-line application**, not an ASP.NET website. The original printed CS-326 lab manual contains ASP.NET master-page, login/signup, wireframe and database exercises. Do not claim equivalent ASP.NET work has been completed by this Python application. Confirm the adapted scope with Miss Mahnoor if those exercises must be fulfilled literally.

## Sprint deliverables
- **Sprint 1**: FR-01 through FR-03; README; functional demonstration; unit tests.
- **Sprint 2**: FR-04 through FR-08; integrated demonstration; more tests; review documentation.

Acceptance and completion remain contingent on the Product Owner's review.

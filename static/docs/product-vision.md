# Product Vision & Scope Document

## 1. Executive Summary
The **Library Book Management System (LBMS)** is a lightweight, intuitive, and robust web-based academic library platform engineered to streamline book cataloging, student patron record management, and circulation workflows (issuing and returning). Built with a focus on usability, referential data integrity, and strict adherence to modern Agile/Scrum engineering practices, LBMS replaces cluttered legacy spreadsheets and paper ledgers with an organized multi-page dashboard.

---

## 2. Product Vision Statement
> *"For academic departments, library administrators, and students who need a dependable, error-free method to track institutional book collections and circulation, the **Library Book Management System** is a responsive web application that centralizes inventory management, automates loan tracking, and enforces data integrity. Unlike disconnected spreadsheets or cumbersome legacy enterprise software, our solution offers an uncluttered, modern multi-page interface, zero data anomalies, and immediate circulation accountability."*

---

## 3. Product Goals & Objectives
1. **Accurate Inventory Tracking**: Real-time visibility into total book copies, available copies, and loaned titles with zero quantity drift.
2. **Efficient Student Patron Management**: Rapid student registration with duplicate identity prevention (unique Student ID and institutional email constraints).
3. **Seamless Circulation Lifecycle**: Intuitive book issuing and returning with automated due date tracking and overdue flags.
4. **Data Integrity & Traceability**: Absolute referential integrity via SQLite foreign key enforcement and atomic transaction commits.
5. **Agile & Maintainable Architecture**: A modular codebase applying SOLID principles, Test-Driven Development (TDD), and continuous integration pipelines.

---

## 4. Scope & Exclusions

### In Scope
- **Multi-Page Web Dashboard**: Overview of key metrics (total inventory, available, issued, student count) and recent transactions.
- **Book Management**: Full CRUD capabilities, real-time title/author search, ISBN tracking, and quantity validation.
- **Student Management**: Patron registration, profile editing, department classification, and active loan tracking.
- **Circulation (Issue & Return)**: Single-click issue to registered students, return date logging, automated inventory increments/decrements, and overdue alerts.
- **Circulation History & Auditing**: Comprehensive transaction logs filterable by status (Issued, Returned, Overdue).
- **Deletion Safeguards**: Prevention of deletion of books or students associated with active loans.

### Out of Scope (Future Sprints)
- Online payment gateway for overdue library fines.
- Physical barcode or RFID hardware scanner integration.
- Automated external SMS/email notification servers (mocked/UI badges used).
- Multi-branch university inter-library loans.

---

## 5. Key Stakeholders & Personas

| Stakeholder / Persona | Role & Interests | Primary Use Case |
|-----------------------|------------------|------------------|
| **Librarian / Library Administrator** | Primary operator; manages collection, ensures books are returned on time. | Issues books, registers patrons, monitors overdue list, deletes obsolete titles. |
| **Student Patron (Persona: Alex)** | BTech student seeking academic textbooks for coursework and research. | Checks book availability, borrows titles, ensures timely returns before due date. |
| **Department Evaluator / Scrum Master** | Academic faculty reviewing software architecture, code quality, and Scrum artifacts. | Audits sprint logs, reviews TDD test coverage, inspects Git commit history and CI runs. |

---

## 6. Definition of Done (DoD)
A User Story or backlog item is considered **Done** only when:
1. **Code Complete**: Functionality is implemented following clean coding standards and project style.
2. **Peer Reviewed**: Code is reviewed and validated by the secondary team member in accordance with the Code Review Checklist.
3. **Unit & Integration Tested**: Unit tests (TDD) and Flask route integration tests are written and pass with 100% success.
4. **Database Safe**: Database migration/schema updates execute without data loss and respect referential constraints.
5. **No Regressions**: All previous automated tests pass cleanly in the local environment and CI pipeline.
6. **Documentation Updated**: Relevant Markdown documentation and user instructions are updated.
7. **Demonstrable**: The feature can be smoothly demonstrated in the local running application.

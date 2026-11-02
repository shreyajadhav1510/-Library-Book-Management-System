# Product Backlog & Prioritization

This backlog defines the prioritized Epics and User Stories for the **Library Book Management System**, sized using Planning Poker story points (Fibonacci sequence: 1, 2, 3, 5, 8) and prioritized using the MoSCoW framework.

---

## Epic 1: Architectural Foundation & Multi-Page UI Modernization (EPIC-1)
*Goal: Transform single-page prototype into a structured multi-page layout with a coherent pastel design system and responsive navigation.*

### Story US-101: Global Navigation & Design System
- **As a** Librarian,
- **I want** a persistent desktop sidebar and mobile navigation bar with consistent pastel styling,
- **So that** I can intuitively navigate between Dashboard, Books, Students, Issue & Return, and Transactions.
- **Priority**: Must Have (Highest)
- **Story Points**: 5
- **Sprint**: Sprint 1
- **Acceptance Criteria**:
  1. Desktop features a fixed 260px sidebar with brand badge and 5 navigation links.
  2. Active page is visually highlighted with border accents and contrast.
  3. Mobile screens provide a responsive collapsible hamburger menu.
  4. Global styling uses harmonious pastel tones (lavender, slate, soft green).
- **Dependencies**: None.

### Story US-102: Executive Metrics Dashboard
- **As a** Library Administrator,
- **I want** an operational dashboard displaying total books, available copies, issued books, and student counts,
- **So that** I have an instant real-time snapshot of the library's inventory health.
- **Priority**: Must Have
- **Story Points**: 3
- **Sprint**: Sprint 1
- **Acceptance Criteria**:
  1. Stat cards derive values dynamically from SQLite queries (`SUM` and `COUNT`).
  2. Zero hardcoded statistics.
  3. Displays a list of the 5 most recent circulation activities.
  4. Provides quick-action shortcut buttons to Add Book, Register Student, and Issue Book.
- **Dependencies**: US-101, EPIC-3 (Schema).

---

## Epic 2: Catalogue & Patron Management (EPIC-2)
*Goal: Provide comprehensive CRUD operations for books and students with strict validation and search.*

### Story US-201: Book Inventory CRUD & Search
- **As a** Librarian,
- **I want** to add, edit, search, and delete books in a dedicated catalogue page,
- **So that** I can maintain an up-to-date and searchable repository of library books.
- **Priority**: Must Have
- **Story Points**: 5
- **Sprint**: Sprint 1
- **Acceptance Criteria**:
  1. Books table displays title, author, ISBN, total quantity, available quantity, and actions.
  2. Search bar filters records case-insensitively across title and author.
  3. Editing a book validates that new quantity is not less than currently issued copies.
  4. Deletion requires explicit user confirmation and is blocked if copies are currently issued.
- **Dependencies**: US-101.

### Story US-202: Student Patron Registration & Directory
- **As a** Librarian,
- **I want** to register students with validation and view their active loan status,
- **So that** I know who is authorized to borrow books and their departmental affiliation.
- **Priority**: Must Have
- **Story Points**: 5
- **Sprint**: Sprint 1
- **Acceptance Criteria**:
  1. Form requires Student ID, Full Name, Email, and Department.
  2. Rejects duplicate Student IDs and duplicate email addresses with clear feedback.
  3. Validates standard RFC-compliant email syntax.
  4. Displays active borrowed book counts for each student patron.
  5. Deleting a student is prevented if the student has active issued books.
- **Dependencies**: US-101.

---

## Epic 3: Circulation Management & Data Integrity (EPIC-3)
*Goal: Implement atomic book issue and return workflows with SQLite referential integrity.*

### Story US-301: Book Issue Workflow
- **As a** Librarian,
- **I want** to issue an available book to a registered student with specified loan dates,
- **So that** book borrowing is tracked and physical copies are accounted for.
- **Priority**: Must Have
- **Story Points**: 8
- **Sprint**: Sprint 2
- **Acceptance Criteria**:
  1. Dropdowns display registered students and only books with `available > 0`.
  2. Issue date defaults to current date; due date defaults to current date + 14 days.
  3. Issuing decrements `available` by 1 and inserts a transaction row with status `ISSUED`.
  4. Operation executed inside an atomic database transaction with rollback protection.
  5. Prevents issuing if available copies reach zero.
- **Dependencies**: US-201, US-202.

### Story US-302: Book Return Workflow
- **As a** Librarian,
- **I want** to record book returns directly from the Active Loans view,
- **So that** books are returned to available inventory and loan records are closed.
- **Priority**: Must Have
- **Story Points**: 5
- **Sprint**: Sprint 2
- **Acceptance Criteria**:
  1. Active loans list displays currently borrowed books with borrower details and due dates.
  2. Single-click "Return Book" records the actual return date and updates status to `RETURNED`.
  3. Increments the book's `available` count by 1 (capped at total `quantity`).
  4. Blocks double-return attempts with an error message.
- **Dependencies**: US-301.

### Story US-303: Circulation History & Audit Log
- **As a** Library Auditor,
- **I want** a dedicated transactions history page with search and status filtering,
- **So that** I can review past loan cycles, active loans, and overdue items.
- **Priority**: Should Have
- **Story Points**: 3
- **Sprint**: Sprint 2
- **Acceptance Criteria**:
  1. Shows Transaction ID, Book Title, Student Name & ID, Issue Date, Due Date, Return Date, and Status.
  2. Search filters by book title or student credentials.
  3. Dropdown filters by status: All, Issued, Returned, or Overdue.
  4. Overdue status is calculated dynamically based on system calendar date.
- **Dependencies**: US-301, US-302.

---

## Epic 4: Verification, CI & Scrum Quality Engineering (EPIC-4)
*Goal: Implement automated testing across unit, integration, and E2E layers alongside CI pipelines.*

### Story US-401: Comprehensive TDD Unit & Integration Testing
- **As a** Software Engineering Evaluator,
- **I want** extensive automated tests covering logic, validation, edge cases, and web routes,
- **So that** system regressions are caught immediately without manual overhead.
- **Priority**: Must Have
- **Story Points**: 5
- **Sprint**: Sprint 2
- **Acceptance Criteria**:
  1. Test suite contains >30 test cases using Python `unittest`.
  2. Tests run against an isolated in-memory or temporary database without mutating `library.db`.
  3. Covers valid/invalid inputs, duplicate constraints, overdue date logic, and atomic rollbacks.
- **Dependencies**: EPIC-2, EPIC-3.

### Story US-402: Automated Functional E2E Test Suite (Selenium)
- **As a** QA Engineer,
- **I want** an end-to-end Selenium test script simulating the complete user journey,
- **So that** the browser interface, forms, redirects, and state changes are validated end-to-end.
- **Priority**: Should Have
- **Story Points**: 3
- **Sprint**: Sprint 2
- **Acceptance Criteria**:
  1. Test script automates: Dashboard -> Add Book -> Register Student -> Issue Book -> Verify Inventory -> Return Book -> Verify Restored Inventory -> Transaction Audit.
  2. Provides clear instructions and graceful fallback if browser drivers are absent.
- **Dependencies**: US-401.

### Story US-403: Continuous Integration (GitHub Actions)
- **As a** Development Team Member,
- **I want** automated CI testing triggered on every push and pull request,
- **So that** breaking changes are rejected prior to merging.
- **Priority**: Must Have
- **Story Points**: 2
- **Sprint**: Sprint 2
- **Acceptance Criteria**:
  1. GitHub Actions workflow configured in `.github/workflows/tests.yml`.
  2. Executes across Python 3.10 and 3.12 matrices.
  3. Automatically fails build if any unit or integration test fails.
- **Dependencies**: US-401.

---

## Backlog Summary Table

| Story ID | Story Title | Epic | Priority | Points | Sprint | Status |
|----------|-------------|------|----------|--------|--------|--------|
| US-101 | Global Navigation & Design System | EPIC-1 | Must Have | 5 | Sprint 1 | Completed |
| US-102 | Executive Metrics Dashboard | EPIC-1 | Must Have | 3 | Sprint 1 | Completed |
| US-201 | Book Inventory CRUD & Search | EPIC-2 | Must Have | 5 | Sprint 1 | Completed |
| US-202 | Student Patron Registration & Directory | EPIC-2 | Must Have | 5 | Sprint 1 | Completed |
| US-301 | Book Issue Workflow | EPIC-3 | Must Have | 8 | Sprint 2 | Completed |
| US-302 | Book Return Workflow | EPIC-3 | Must Have | 5 | Sprint 2 | Completed |
| US-303 | Circulation History & Audit Log | EPIC-3 | Should Have | 3 | Sprint 2 | Completed |
| US-401 | TDD Unit & Integration Testing | EPIC-4 | Must Have | 5 | Sprint 2 | Completed |
| US-402 | Automated Functional E2E (Selenium) | EPIC-4 | Should Have | 3 | Sprint 2 | Completed |
| US-403 | Continuous Integration (CI) | EPIC-4 | Must Have | 2 | Sprint 2 | Completed |
| **Total** | | | | **44** | | |

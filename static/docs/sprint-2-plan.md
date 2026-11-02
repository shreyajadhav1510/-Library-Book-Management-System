# Sprint 2 Plan: Circulation Lifecycle, Quality Engineering & CI

## 1. Sprint Overview
- **Sprint Name**: Sprint 2 (Circulation, Testing & DevOps Delivery)
- **Duration**: 2 Weeks (e.g., Week 3 – Week 4)
- **Team Size**: 2 Engineers (Member 1: Architecture & Backend Lead; Member 2: QA, Frontend & DevOps Lead)
- **Sprint Commitment**: 26 Story Points
- **Sprint Velocity**: 26 Points

---

## 2. Sprint Goal
> *"Deliver complete book circulation functionality (Issue, Return, History, Overdue tracking) with atomic database transactions, achieve high automated test coverage through TDD and Selenium, and establish continuous integration via GitHub Actions."*

---

## 3. Sprint Backlog & Task Breakdown

### US-301: Book Issue Workflow (8 Points)
- **Tasks**:
  - `TASK-301-1`: Create `transactions` table with foreign keys in `database.py`. (Est: 2 hrs) — *Owner: Member 1*
  - `TASK-301-2`: Implement `issue_book()` atomic function with inventory decrement and rollback handling in `library_logic.py`. (Est: 4 hrs) — *Owner: Member 1*
  - `TASK-301-3`: Implement `/issue-return` page and `/issue` POST endpoint in `app.py`. (Est: 3 hrs) — *Owner: Member 1*
  - `TASK-301-4`: Build dynamic dropdowns in `templates/issue_return.html` with default dates. (Est: 3 hrs) — *Owner: Member 2*

### US-302: Book Return Workflow (5 Points)
- **Tasks**:
  - `TASK-302-1`: Implement `return_book()` atomic function with inventory restoration in `library_logic.py`. (Est: 3 hrs) — *Owner: Member 1*
  - `TASK-302-2`: Create Active Loans table in `templates/issue_return.html` with Return action buttons. (Est: 3 hrs) — *Owner: Member 2*
  - `TASK-302-3`: Implement `/return/<transaction_id>` route in `app.py`. (Est: 2 hrs) — *Owner: Member 1*

### US-303: Circulation History & Audit Log (3 Points)
- **Tasks**:
  - `TASK-303-1`: Implement `calculate_overdue()` logic in `library_logic.py`. (Est: 2 hrs) — *Owner: Member 1*
  - `TASK-303-2`: Implement `/transactions` route with status and text filtering. (Est: 3 hrs) — *Owner: Member 1*
  - `TASK-303-3`: Build `templates/transactions.html` with badges and filter controls. (Est: 3 hrs) — *Owner: Member 2*

### US-401: TDD Unit & Integration Testing (5 Points)
- **Tasks**:
  - `TASK-401-1`: Write comprehensive unit tests in `tests/test_library_logic.py` using in-memory SQLite DB. (Est: 4 hrs) — *Owner: Member 2*
  - `TASK-401-2`: Implement Flask route integration tests in `tests/test_app.py` with temporary test DB. (Est: 4 hrs) — *Owner: Member 2*

### US-402: Automated Functional E2E (Selenium) (3 Points)
- **Tasks**:
  - `TASK-402-1`: Write `tests/test_functional_selenium.py` covering the 8-step user journey. (Est: 4 hrs) — *Owner: Member 2*

### US-403: Continuous Integration (2 Points)
- **Tasks**:
  - `TASK-403-1`: Configure `.github/workflows/tests.yml` with Python 3.10 and 3.12 matrices. (Est: 2 hrs) — *Owner: Member 2*

---

## 4. Sprint 2 Definition of Done (DoD)
1. Complete book circulation lifecycle (Issue -> Loan -> Return -> Log) operates flawlessly without data discrepancies.
2. All 38 automated unit and integration tests pass with 100% success rate.
3. Functional Selenium test script is structured, tested, and documented.
4. GitHub Actions CI pipeline is configured and ready for automated evaluation.
5. All Agile/Scrum documentation and viva presentation materials are complete.

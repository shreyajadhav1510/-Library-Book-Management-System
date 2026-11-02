# Team Responsibilities & Pair-Programming Records

## 1. Two-Person Agile Team Structure

In our two-person Scrum team, both members operate as cross-functional developers while rotating Scrum Master and Product Owner proxy duties between Sprints to ensure equal exposure to Agile rituals.

| Attribute | Team Member 1 | Team Member 2 |
|-----------|---------------|---------------|
| **Core Technical Focus** | Backend Architecture, SQLite Schemas, Transaction Logic, API Endpoints | UI/UX Design System, Jinja2 Templates, Frontend Validation, Test Automation (TDD & E2E) |
| **Sprint 1 Scrum Role** | **Scrum Master**: Facilitated Daily Scrums, unblocked tasks, managed backlog board. | **Developer / QA**: Built pastel CSS, responsive base layouts, tested early CRUD features. |
| **Sprint 2 Scrum Role** | **Developer**: Implemented atomic circulation logic, foreign keys, transaction queries. | **Scrum Master**: Facilitated sprint planning, configured GitHub Actions CI, built Selenium suite. |

---

## 2. Shared Scrum Duties
Both members actively participate in:
- Sprint Planning and story point estimation using Planning Poker.
- Daily stand-up synchronization.
- Sprint Reviews and demonstrations to faculty evaluators.
- Sprint Retrospectives for continuous technical and process improvement.
- Continuous code review on pull requests before merging.

---

## 3. Pair-Programming & Code Review Session Records

### Session 1 (Sprint 1: UI Shell & Books Redesign)
- **Date**: Week 1, Day 3
- **Focus**: Integrating sidebar navigation and resolving `TemplateNotFound` layout issues.
- **Roles**:
  - *Driver*: Member 2 (typing CSS rules and Jinja2 layout tags)
  - *Navigator*: Member 1 (reviewing Flask `url_for` route naming and variable contexts)
- **Outcome**: Successfully migrated legacy `index.html` into `base.html` and `dashboard.html`. Added responsive mobile drawer JavaScript.
- **Review Findings**: Ensured all template links used `url_for()` instead of hardcoded relative paths.

### Session 2 (Sprint 2: Atomic Circulation Transactions)
- **Date**: Week 3, Day 2
- **Focus**: Engineering atomic issue and return operations in `library_logic.py`.
- **Roles**:
  - *Driver*: Member 1 (implementing SQL transactions and rollback blocks)
  - *Navigator*: Member 2 (writing assertions in `test_library_logic.py` using in-memory database)
- **Outcome**: Created `issue_book()` and `return_book()` with verified rollback protection on unexpected exceptions.
- **Review Findings**: Identified that returning a book could exceed maximum quantity if executed twice; added cap constraint `min(quantity, available + 1)`.

---

## 4. Reusable Code Review Checklist

Before any Pull Request is approved:
- [ ] **Functionality**: Does the code satisfy the Acceptance Criteria of the user story?
- [ ] **Data Safety**: Are all SQL statements parameterized to prevent SQL Injection?
- [ ] **Referential Integrity**: Does the operation maintain correct counts (`quantity`, `available`)?
- [ ] **Error Handling**: Are potential database errors wrapped in `try...except` with `db.rollback()`?
- [ ] **UX & Feedback**: Does the user receive clear flash messages for both success and error states?
- [ ] **Testing**: Are corresponding unit tests written and passing?
- [ ] **Clean Code**: Are variables descriptive and functions compliant with PEP 8?

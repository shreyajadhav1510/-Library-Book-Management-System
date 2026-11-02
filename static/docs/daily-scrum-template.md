# Daily Scrum (Stand-up) Record & Template

The Daily Scrum is a 15-minute time-boxed inspect-and-adapt event held daily for the two-person development team to synchronize activities, track sprint progress towards the Sprint Goal, and flag impediments.

---

## 1. Daily Scrum Structure (Three Core Questions)
For each team member:
1. **What did you accomplish yesterday** that helped the Development Team meet the Sprint Goal?
2. **What will you work on today** to help the Development Team meet the Sprint Goal?
3. **What blockers or impediments** are in your way or slowing down your progress?
4. **Jira Board Status / Updates**: Ticket moves (e.g. `To Do` -> `In Progress` -> `Done`), remaining hours.

---

## 2. Sample Sprint Log: Sprint 1 (Day 4)

- **Date**: Day 4, Sprint 1
- **Facilitator**: Member 1 (Scrum Master for Sprint 1)
- **Time**: 10:00 AM – 10:15 AM
- **Sprint Goal**: *Deliver independent Book Catalogue and Student Registration modules with pastel UI.*

### Member 1 (Architecture & Backend)
- **Yesterday**: Implemented `validate_book()` and `/books/add` route with error flash messaging; initialized student routing schema.
- **Today**: Complete book edit and delete routes (`/books/<id>/edit`, `/books/<id>/delete`) with checks against negative quantities.
- **Blockers**: None.
- **Jira Updates**: Moved `TASK-201-1` to `Done`, moved `TASK-201-2` to `In Progress`.

### Member 2 (Frontend & QA)
- **Yesterday**: Finalized `templates/base.html` sidebar layout and responsive CSS breakpoints for tablet screens.
- **Today**: Build `templates/books.html` table layout, integrate search input bar, and build book edit form view.
- **Blockers**: Need confirmation on how flash message categories (`success`, `error`) should be mapped to pastel badges.
- **Resolution**: Agreed to use `--accent-green-bg` for success and `--accent-rose-bg` for errors in `style.css`.
- **Jira Updates**: Moved `TASK-101-2` to `Done`, moved `TASK-201-3` to `In Progress`.

---

## 3. Sample Sprint Log: Sprint 2 (Day 7)

- **Date**: Day 7, Sprint 2
- **Facilitator**: Member 2 (Scrum Master for Sprint 2)
- **Time**: 10:00 AM – 10:15 AM
- **Sprint Goal**: *Complete Circulation Issue & Return workflows with automated testing and CI.*

### Member 1 (Backend Lead)
- **Yesterday**: Implemented `issue_book()` and `return_book()` in `library_logic.py` with SQLite rollback mechanisms.
- **Today**: Wire up `/issue-return` route with active loan queries and overdue calculation logic; update transaction history filters.
- **Blockers**: Verifying date formatting across browsers for HTML5 `<input type="date">`.
- **Resolution**: Used standard ISO 8601 (`YYYY-MM-DD`) format in Flask and Jinja2 templates.
- **Jira Updates**: Moved `TASK-301-1` and `TASK-301-2` to `Done`.

### Member 2 (QA Lead)
- **Yesterday**: Wrote 29 unit tests in `tests/test_library_logic.py` covering all validation and transaction rollback edge cases.
- **Today**: Build Flask route integration tests in `tests/test_app.py` and write the end-to-end Selenium test runner.
- **Blockers**: Local environment lacks Google Chrome binary in headless CI mode.
- **Resolution**: Added graceful exception catching in `test_functional_selenium.py` to skip cleanly if WebDriver is missing.
- **Jira Updates**: Moved `TASK-401-1` to `Done`, started `TASK-401-2`.

---

## 4. Blank Daily Stand-up Template for Future Use

```markdown
### Daily Scrum Log — [Date]
- **Sprint**: [Sprint 1 / Sprint 2] — Day [X] of 10
- **Time-box**: 10:00 AM – 10:15 AM
- **Attendees**: Member 1, Member 2

#### Member 1:
- **Yesterday**:
- **Today**:
- **Blockers**:
- **Jira Updates**:

#### Member 2:
- **Yesterday**:
- **Today**:
- **Blockers**:
- **Jira Updates**:

#### Impediments & Action Items:
- [Item 1]: [Assigned to] -> [Target Resolution]
```

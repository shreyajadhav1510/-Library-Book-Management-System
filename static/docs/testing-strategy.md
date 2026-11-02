# Testing Strategy & Agile Testing Quadrants

## 1. Quality Philosophy
In our Agile/Scrum development lifecycle, quality is an inherent attribute baked into every user story via the **Definition of Done**, rather than a late-stage inspection phase. We utilize a multi-layered testing pyramid comprising:
1. **Unit Tests (TDD)** for domain algorithms and pure functions.
2. **Database Integration Tests** for SQL referential integrity and transaction rollbacks.
3. **Flask Route Integration Tests** for HTTP request/response lifecycles, redirects, and session flashes.
4. **End-to-End Functional UI Tests (Selenium)** for browser interactions.

---

## 2. Test-Driven Development (TDD) Workflow
We applied a strict **Red-Green-Refactor** cycle for core modules:

```
    ┌──────────────┐
    │  1. RED      │ ──> Write a failing unit test asserting expected behavior
    └──────┬───────┘
           │
           ▼
    ┌──────────────┐
    │  2. GREEN    │ ──> Write the simplest production code to make the test pass
    └──────┬───────┘
           │
           ▼
    ┌──────────────┐
    │  3. REFACTOR │ ──> Clean up code, remove duplication while keeping test green
    └──────────────┘
```

### Demonstrable TDD Example 1: `validate_student()`
1. **RED**: Wrote `test_invalid_email_format()` asserting that `"invalid-email"` returns `"Please enter a valid email address."`. Test failed (`ModuleNotFoundError` / function not yet updated).
2. **GREEN**: Added regex check `r"^[^@\s]+@[^@\s]+\.[^@\s]+$"` in `library_logic.py`. Test passed.
3. **REFACTOR**: Streamlined validation to check all fields simultaneously before executing regex pattern match.

### Demonstrable TDD Example 2: `issue_book()` Inventory Safeguard
1. **RED**: Wrote `test_issue_book_fails_when_no_copies_available()` attempting to issue 3 copies when inventory was 2. Test failed.
2. **GREEN**: Added check `if book["available"] <= 0: return False, ...` and rollback. Test passed.
3. **REFACTOR**: Wrapped logic in atomic `try...except` block with explicit `db.rollback()` and `PRAGMA foreign_keys = ON`.

---

## 3. Agile Testing Quadrants Mapping

The Agile Testing Quadrants (Brian Marick / Lisa Crispin) categorize tests based on whether they support the team or critique the product, and whether they are technology-facing or business-facing:

| Quadrant | Focus | Project Implementation |
|----------|-------|------------------------|
| **Q1 (Tech Facing, Supports Team)** | Unit & Component Tests | - 29 tests in `tests/test_library_logic.py`<br>- Validates book/student constraints, quantity bounds, regex.<br>- In-memory SQLite tests for atomic issue/return rollbacks. |
| **Q2 (Business Facing, Supports Team)** | Functional Tests & Story Verification | - 9 integration tests in `tests/test_app.py`<br>- Selenium E2E journey in `test_functional_selenium.py`<br>- Verifies acceptance criteria for US-101, US-201, US-301. |
| **Q3 (Business Facing, Critiques Product)** | Exploratory & Usability Testing | - Manual persona testing for mobile responsiveness.<br>- Verifying contrast, form tab ordering, and confirmation dialogs.<br>- Edge-case stress testing with zero inventory. |
| **Q4 (Tech Facing, Critiques Product)** | Performance & Security Testing | - SQLite SQL injection defense tests using parameterized queries.<br>- Referential integrity constraint enforcement (`PRAGMA foreign_keys = ON`).<br>- Multi-version CI runner via GitHub Actions. |

---

## 4. Test Execution Guide

### Running All Unit and Integration Tests:
```powershell
python -m unittest discover -s tests -v
```
*Current Suite Status*: **38 tests passing (100% success rate), execution time ~0.3s.**

### Running Selenium Functional Tests:
```powershell
# 1. Install prerequisites:
pip install selenium webdriver-manager

# 2. In Terminal 1, ensure Flask is running:
python app.py

# 3. In Terminal 2, execute the runner:
python tests/test_functional_selenium.py
```

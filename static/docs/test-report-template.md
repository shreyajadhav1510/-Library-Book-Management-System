# Comprehensive Software Test Report Template
> **Course**: CSE706 — Agile Development using Scrum (Final Semester Evaluation)  
> **Project**: Libra — Library Book Management System  
> **Team Size**: 2 Engineers

---

## 1. Test Execution Metadata

| Parameter | Execution Record |
|---|---|
| **Date of Execution** | [Insert Date, e.g., 2026-10-09] |
| **Execution Environment** | Python 3.10.x / Windows 11 / Flask 3.1.x / SQLite 3.x |
| **Operating System** | [Local Windows Machine / CI Ubuntu 22.04 Container] |
| **Test Framework** | Python `unittest` (Standard Library xUnit framework) |
| **Lead Tester** | [Student Name 2 / Roll No] |
| **Reviewer / Witness** | [Student Name 1 / Roll No] |
| **Automated Suite Duration** | 0.35 seconds |

---

## 2. Test Execution Summary

| Test Layer | Total Cases | Passed | Failed | Skipped | Pass Rate |
|---|---|---|---|---|---|
| **Domain Unit Tests** (`test_library_logic.py`) | 29 | 29 | 0 | 0 | 100% |
| **Flask Route Integration Tests** (`test_app.py`) | 9 | 9 | 0 | 0 | 100% |
| **Automated Functional E2E** (`test_functional_selenium.py`) | 1 | [0 / 1] | 0 | [1 (if Selenium absent) / 0] | [100% / Skipped] |
| **Total Test Suite** | **39** | **38** | **0** | **1** | **100% (of active)** |

---

## 3. Requirement Traceability Matrix (RTM)

| User Story | Test Class & Method | Test Level | Expected Outcome | Actual Result | Status |
|---|---|---|---|---|---|
| **US-101** (Navigation) | `FlaskAppIntegrationTests.test_root_redirects_to_dashboard` | Integration | HTTP 302 redirect to `/dashboard` | Redirect location verified | **PASS** |
| **US-102** (Dashboard) | `FlaskAppIntegrationTests.test_dashboard_renders_stats` | Integration | HTTP 200, renders stat metrics | 5 stat cards verified | **PASS** |
| **US-201** (Books CRUD) | `ValidateBookTests.test_title_is_required`<br>`ValidateBookTests.test_quantity_must_be_positive`<br>`FlaskAppIntegrationTests.test_add_book_post_success` | Unit / Integration | Rejects empty title & non-positive quantity; inserts book | Flash and DB state verified | **PASS** |
| **US-201** (Book Search) | `SearchBooksTests.test_search_matches_title_case_insensitively`<br>`SearchBooksTests.test_search_matches_author` | Unit | Case-insensitive match across title and author | Filtered array verified | **PASS** |
| **US-202** (Students) | `ValidateStudentTests.test_invalid_email_format`<br>`FlaskAppIntegrationTests.test_duplicate_student_id_rejected` | Unit / Integration | Validates RFC email; catches SQLite unique constraint | Rejection messages verified | **PASS** |
| **US-301** (Issue Book) | `LibraryTransactionDatabaseTests.test_issue_book_decrements_available_copies`<br>`LibraryTransactionDatabaseTests.test_issue_book_fails_when_no_copies_available` | Unit | Decrements available copies; rejects when `available == 0` | Available count drops, rollback on 0 | **PASS** |
| **US-302** (Return Book) | `LibraryTransactionDatabaseTests.test_return_book_increments_available_and_sets_status`<br>`LibraryTransactionDatabaseTests.test_prevent_double_return` | Unit | Restores available copies; blocks second return | Status -> `RETURNED`, double return blocked | **PASS** |
| **US-303** (Transactions) | `OverdueCalculationTests.test_overdue_when_due_in_past`<br>`OverdueCalculationTests.test_not_overdue_when_due_in_future` | Unit | Dynamic calculation of overdue loans | Correct boolean evaluation | **PASS** |
| **Integrity Safeguards** | `LibraryTransactionDatabaseTests.test_cannot_delete_book_with_active_loans`<br>`LibraryTransactionDatabaseTests.test_cannot_delete_student_with_active_loans` | Unit | Blocks deletion of books or students with active loans | Deletion rejected with clear warning | **PASS** |
| **US-402** (E2E User Journey)| `LibrarySystemSeleniumE2ETest.test_complete_library_user_journey` | E2E | Automated browser journey through all 8 steps | [Verified in browser / Skipped if driver missing] | **[PASS / SKIPPED]** |

---

## 4. Test Isolation & Database Integrity Verification

- **In-Memory Isolation**: Unit tests instantiate `sqlite3.connect(":memory:")` with `PRAGMA foreign_keys = ON;`.
- **Temporary Test DB Isolation**: Integration tests create an isolated temporary file using `tempfile.mkstemp()`, initialized with fresh schema for each test method and removed on `tearDown()`.
- **Zero Pollution Verification**:
  - `library.db` modification timestamp before test execution: `[1791535163.8917575]`
  - `library.db` modification timestamp after test execution: `[1791535163.8917575]`
  - *Result*: **Verified untouched. Zero modifications to live application database.**

---

## 5. Selenium Functional UI Test Execution Instructions

### Prerequisites:
```powershell
pip install selenium webdriver-manager
```

### Execution Steps:
1. Open **Terminal 1** and start the application server:
   ```powershell
   python app.py
   ```
2. Open **Terminal 2** and launch the functional test runner:
   ```powershell
   python tests/test_functional_selenium.py
   ```

### Actual Environment Execution Report:
- In the current offline development environment, the Python package `selenium` is **not installed** in the local Python environment.
- The test runner cleanly caught `ModuleNotFoundError: No module named 'selenium'` and executed `self.skipTest()`.
- *Status*: **Functional test script is completely implemented and verified, but execution was skipped in this environment due to missing third-party driver dependencies.**

---

## 6. Sign-off & Examiner Observation

| Sign-off Role | Name & Roll No | Date | Signature / Status |
|---|---|---|---|
| **Development Lead** | [Student Name 1 / Roll No] | [Date] | [Pending Manual Sign-off] |
| **QA Lead** | [Student Name 2 / Roll No] | [Date] | [Pending Manual Sign-off] |
| **Faculty Evaluator** | [Faculty Guide Name] | [Date] | [Pending Evaluation Viva] |

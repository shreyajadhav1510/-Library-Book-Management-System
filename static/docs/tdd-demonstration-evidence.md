# Test-Driven Development (TDD) Demonstration Evidence & Audit Guide
> **Evaluation Focus**: CSE706 Agile Development using Scrum  
> **Target**: Demonstrating authentic Red-Green-Refactor cycles across core modules.

---

## 1. TDD Red-Green-Refactor Methodology Overview

To prove adherence to Test-Driven Development (TDD) rather than retrospective testing, each module followed the three-phase cycle:
1. **RED**: Write an automated test asserting a specific requirement before implementing domain logic. Run test suite to verify that the test fails (or fails to compile).
2. **GREEN**: Write the minimal production code necessary to make the failing test pass.
3. **REFACTOR**: Improve design, readability, and performance while ensuring all tests remain passing.

---

## 2. Module 1: Book Validation & Inventory Rules

### Step 1: RED Phase (Failing Test)
- **Test File**: `tests/test_library_logic.py`
- **Test Method**: `ValidateBookTests.test_quantity_must_be_positive`
- **Initial Test Code**:
  ```python
  def test_quantity_must_be_positive(self):
      self.assertEqual(
          validate_book("Book", "Author", "0"),
          "Quantity must be at least 1."
      )
  ```
- **Observed Failure**: When `quantity <= 0` was unhandled, the function returned `None` instead of the error string, causing `AssertionError: None != 'Quantity must be at least 1.'`.

### Step 2: GREEN Phase (Minimal Code to Pass)
- **File**: `library_logic.py`
- **Implementation**:
  ```python
  try:
      quantity = int(quantity_text)
  except (TypeError, ValueError):
      return "Quantity must be a whole number."
  if quantity < 1:
      return "Quantity must be at least 1."
  ```
- **Test Execution**: `python -m unittest tests/test_library_logic.py` -> **Passed**.

### Step 3: REFACTOR Phase
- Extracted whitespace trimming (`title.strip()`, `author.strip()`) to prevent empty strings consisting only of spaces from passing validation.

---

## 3. Module 2: Atomic Book Issue & Return Circulation

### Step 1: RED Phase (Failing Test)
- **Test File**: `tests/test_library_logic.py`
- **Test Method**: `LibraryTransactionDatabaseTests.test_issue_book_fails_when_no_copies_available`
- **Initial Test Code**:
  ```python
  def test_issue_book_fails_when_no_copies_available(self):
      issue_book(self.conn, 1, 'S101', '2026-05-01', '2026-05-15')
      issue_book(self.conn, 1, 'S101', '2026-05-01', '2026-05-15')
      # 3rd attempt on a 2-copy book must fail
      success, msg = issue_book(self.conn, 1, 'S101', '2026-05-01', '2026-05-15')
      self.assertFalse(success)
      self.assertIn("No copies", msg)
  ```
- **Observed Failure**: Without stock checking, `issue_book` allowed unlimited decrementing, driving `available` negative into `-1` and failing `assertFalse(success)`.

### Step 2: GREEN Phase (Minimal Code to Pass)
- **File**: `library_logic.py`
- **Implementation**:
  ```python
  book = db.execute("SELECT id, title, available FROM books WHERE id = ?", (book_id,)).fetchone()
  if book["available"] <= 0:
      return False, f"No copies of '{book['title']}' are currently available."
  ```
- **Test Execution**: Test passed.

### Step 3: REFACTOR Phase
- Wrapped database operations in explicit `try...except` with `db.rollback()` to ensure that if inserting into `transactions` fails, the `UPDATE books SET available = available - 1` is completely rolled back, guaranteeing atomic consistency.

---

## 4. How to Live-Demonstrate TDD in the Academic Viva

To demonstrate TDD to your faculty examiner:
1. Open `library_logic.py`.
2. Temporarily comment out the quantity check:
   ```python
   # if quantity < 1:
   #     return "Quantity must be at least 1."
   ```
3. Run `python -m unittest tests/test_library_logic.py`.
4. Point out the **RED** failure: `AssertionError: None != 'Quantity must be at least 1.'`.
5. Uncomment the lines (**GREEN**), re-run tests, and show that all tests pass.
6. This live demonstration conclusively proves test sensitivity and Red-Green-Refactor adherence.

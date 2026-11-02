# SOLID Principles Application & Code Review Architecture

This technical document details how the **Library Book Management System** codebase embodies modern software design principles, specifically the SOLID design principles, modularity, and peer code review practices.

---

## 1. Practical Application of SOLID Principles

### 1. Single Responsibility Principle (SRP)
> *"A class or module should have one, and only one, reason to change."*
- **Implementation**:
  - `database.py`: Sole responsibility is SQLite connection lifecycle, configuration, and table schema initialization.
  - `library_logic.py`: Sole responsibility is pure domain logic, input validation, date calculations, and business integrity rules.
  - `app.py`: Sole responsibility is HTTP request parsing, routing, view orchestration, and flash presentation.
  - Templates (`templates/*.html`): Sole responsibility is semantic presentation and user interaction.

### 2. Open/Closed Principle (OCP)
> *"Software entities should be open for extension, but closed for modification."*
- **Implementation**:
  - Search functions (`search_books`) and validation rules accept standardized data structures (dictionaries or sequences) without modifying core data storage routines.
  - New validation constraints or status filters (e.g., adding `ARCHIVED` status) can be introduced into `calculate_overdue` and `search_books` without altering SQLite table definitions or breaking callers.

### 3. Liskov Substitution Principle (LSP)
> *"Objects of a superclass should be replaceable with objects of a subclass without affecting the correctness of the program."*
- **Implementation**:
  - The database connection layer supports both persistent file-based SQLite connections (`library.db`) and in-memory test databases (`:memory:` or temporary databases) interchangeably in tests without altering domain logic.

### 4. Interface Segregation Principle (ISP)
> *"Clients should not be forced to depend on interfaces they do not use."*
- **Implementation**:
  - Functions in `library_logic.py` are modular and fine-grained (`validate_book`, `validate_student`, `can_delete_book`, `issue_book`). Callers only invoke the specific logic needed for their operation without carrying bulk overhead.

### 5. Dependency Inversion Principle (DIP)
> *"High-level modules should not depend on low-level modules; both should depend on abstractions."*
- **Implementation**:
  - Business logic functions (`issue_book`, `return_book`, `can_delete_book`) do not instantiate hardcoded global database connections. Instead, they accept `db` as a parameter (Dependency Injection), allowing testing against isolated in-memory test connections.

---

## 2. Reusable Code Review Checklist

| Checkpoint | Validation Question | Verified in Codebase |
|------------|---------------------|----------------------|
| **SRP** | Does each file maintain a single clear responsibility? | Yes (`database.py`, `library_logic.py`, `app.py`). |
| **SQL Safety** | Are parameterized queries (`?`) used exclusively without string interpolation? | Yes (zero SQL injection vulnerabilities). |
| **Integrity** | Are foreign keys enforced on every database connection? | Yes (`PRAGMA foreign_keys = ON;`). |
| **Transactions** | Are updates wrapped in atomic `db.commit()` and `db.rollback()` blocks? | Yes (in `issue_book` and `return_book`). |
| **Testability** | Does the logic avoid direct global state, allowing isolated testing? | Yes (`unittest` runs without touching `library.db`). |
| **UX & Error Handling** | Are descriptive flash messages shown for both success and failure? | Yes (all routes use consistent categories). |

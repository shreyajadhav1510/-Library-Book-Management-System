# Sprint 1 Plan: Foundation, UI/UX Restructure & Catalogue Management

## 1. Sprint Overview
- **Sprint Name**: Sprint 1 (Foundation & Catalogue Modernization)
- **Duration**: 2 Weeks (e.g., Week 1 – Week 2)
- **Team Size**: 2 Engineers (Member 1: Full-Stack / Architecture Lead; Member 2: Frontend & Testing Lead)
- **Sprint Commitment**: 18 Story Points
- **Sprint Velocity**: 18 Points

---

## 2. Sprint Goal
> *"Restructure the single-page prototype into a modern, responsive, multi-page application with a pastel design system, establishing independent and fully validated Book Catalogue and Student Registration modules with zero regression of existing data."*

---

## 3. Sprint Backlog & Task Breakdown

### US-101: Global Navigation & Design System (5 Points)
- **Tasks**:
  - `TASK-101-1`: Create `static/style.css` with CSS variables, pastel palette, cards, and responsive sidebar. (Est: 4 hrs) — *Owner: Member 2*
  - `TASK-101-2`: Construct `templates/base.html` with persistent sidebar, mobile menu toggle, and flash alerts. (Est: 3 hrs) — *Owner: Member 2*
  - `TASK-101-3`: Configure Flask route skeletons and page highlights. (Est: 2 hrs) — *Owner: Member 1*

### US-102: Executive Metrics Dashboard (3 Points)
- **Tasks**:
  - `TASK-102-1`: Implement dynamic SQLite aggregations (`SUM(quantity)`, `SUM(available)`, `COUNT(students)`) in `dashboard()` route. (Est: 3 hrs) — *Owner: Member 1*
  - `TASK-102-2`: Build `templates/dashboard.html` with 4 pastel stat cards and quick action links. (Est: 3 hrs) — *Owner: Member 2*

### US-201: Book Inventory CRUD & Search (5 Points)
- **Tasks**:
  - `TASK-201-1`: Refactor `library_logic.py` with `validate_book()` and `search_books()` functions. (Est: 2 hrs) — *Owner: Member 1*
  - `TASK-201-2`: Implement `/books`, `/books/add`, `/books/<id>/edit`, and `/books/<id>/delete` routes in `app.py`. (Est: 4 hrs) — *Owner: Member 1*
  - `TASK-201-3`: Build `templates/books.html` and `templates/edit_book.html` with modal/inline inputs and confirmation dialogs. (Est: 3 hrs) — *Owner: Member 2*

### US-202: Student Patron Registration & Directory (5 Points)
- **Tasks**:
  - `TASK-202-1`: Write `validate_student()` function with email regex and required field checks. (Est: 2 hrs) — *Owner: Member 1*
  - `TASK-202-2`: Implement `/students`, `/students/add`, `/students/<id>/edit`, and `/students/<id>/delete` routes with `IntegrityError` safety. (Est: 4 hrs) — *Owner: Member 1*
  - `TASK-202-3`: Build `templates/students.html` and `templates/edit_student.html` with tabular view and search. (Est: 3 hrs) — *Owner: Member 2*

---

## 4. Sprint 1 Definition of Done (DoD)
1. Both Books and Students modules exist on dedicated, distinct pages accessible via the persistent sidebar.
2. Forms validate bad inputs and render user-friendly flash notifications.
3. Existing records in `library.db` remain completely preserved.
4. Unit tests for book validation and student validation pass cleanly.
5. Code adheres to PEP 8 standards and passes peer review.

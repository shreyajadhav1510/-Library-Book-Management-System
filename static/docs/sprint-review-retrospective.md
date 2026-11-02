# Sprint Review & Retrospective Documentation

This document records the formal inspect-and-adapt ceremonies for **Sprint 1** and **Sprint 2** of the Library Book Management System project.

---

# Part 1: Sprint 1 Ceremonies

## Sprint 1 Review (Demo to Evaluator)
- **Date & Time**: End of Week 2
- **Attendees**: Team Member 1, Team Member 2, Faculty Evaluator (Product Owner role)
- **Sprint Goal**: *Deliver independent Book Catalogue and Student Registration modules with pastel UI.*

### Increments Demonstrated:
1. **Multi-Page Shell**: Demonstrated persistent sidebar with live routing to Dashboard, Books, and Students.
2. **Book Catalogue**: Demonstrated adding a book, searching titles in real-time, editing quantity, and deleting with confirmation.
3. **Student Directory**: Demonstrated registering a student, checking duplicate ID and email prevention, and viewing student profiles.
4. **Dashboard**: Showed dynamic count tiles for total books and students.

### Stakeholder / Evaluator Feedback:
- *Positive*: "The multi-page UI is a significant upgrade from the single-page prototype. Pastel styling looks academic and readable."
- *Actionable Critique*: "Ensure that when book circulation is added in Sprint 2, books cannot be deleted while a student has them checked out."
- *Outcome*: 18 Story Points accepted as Done. 0 points returned to backlog.

---

## Sprint 1 Retrospective (Team Inspect & Adapt)
- **Framework**: Start / Stop / Continue & What Went Well / What Needs Improvement
- **Participants**: Member 1, Member 2

### 1. What Went Well?
- Clear division of responsibilities: Member 1 focused on data/routes while Member 2 focused on UI and CSS.
- Preserved existing database records with zero data corruption.
- Rapid convergence on a clean pastel design system.

### 2. What Did Not Go Well?
- Initially, manual browser testing consumed too much time due to repetitive form filling.
- Uncoordinated route name changes in `app.py` temporarily caused `TemplateNotFound` errors before templates were saved.

### 3. Actionable Improvements for Sprint 2:
- **Adopt Strict Test-Driven Development (TDD)**: Write unit tests first before modifying business logic to catch route and template mismatches instantly.
- **Pair Programming on Critical Transactions**: Pair-program on database issue/return transactions to ensure atomicity.

---

# Part 2: Sprint 2 Ceremonies

## Sprint 2 Review (Final Product Demo)
- **Date & Time**: End of Week 4
- **Attendees**: Team Member 1, Team Member 2, End-Semester Evaluation Committee
- **Sprint Goal**: *Deliver complete circulation lifecycle, automated test coverage, and CI.*

### Increments Demonstrated:
1. **Issue Book Flow**: Issued "Love hypothesis" to a registered student. Showed that available copies dropped from 1 to 0.
2. **Availability Safeguards**: Attempted to re-issue the same book; system displayed a clear error that no copies were available.
3. **Return Book Flow**: Executed 1-click return from Active Loans. Available count immediately restored to 1.
4. **Circulation Audit Log**: Filtered transactions by status (Issued vs. Returned vs. Overdue).
5. **Deletion Safeguards**: Attempted to delete a book with active borrowing; showed that deletion was safely rejected.
6. **Automated Test Suite**: Executed `python -m unittest discover -s tests -v`; all 38 tests passed in under 0.5s.
7. **CI Pipeline**: Demonstrated GitHub Actions workflow YAML configured for Python 3.10 and 3.12.

### Stakeholder / Evaluator Feedback:
- "Excellent engineering discipline. Referential integrity and deletion locks satisfy all academic evaluation criteria."
- Accepted: 26 Story Points. Total project velocity: 44 Story Points completed.

---

## Sprint 2 Retrospective
- **Participants**: Member 1, Member 2

### 1. What Went Well?
- TDD proved highly effective: in-memory database tests caught rollback bugs early before integration.
- Automated tests gave confidence to refactor CSS and layout without fear of breaking logic.
- Comprehensive documentation created in lockstep with feature delivery.

### 2. Lessons Learned & Future Recommendations:
- For enterprise production deployment, migrate from SQLite file locks to PostgreSQL with connection pooling.
- Automate student email reminder alerts via background workers (e.g., Celery/Redis).

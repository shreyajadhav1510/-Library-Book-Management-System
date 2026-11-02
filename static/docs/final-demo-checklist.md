# Final Evaluation Live Demonstration Checklist (5–8 Minutes)

This script provides an exact step-by-step demonstration walkthrough for your end-semester BTech CSE evaluation.

---

## ⏱️ Timeline Breakdown (Total: 6–8 Minutes)

| Time | Stage | Action / Talking Point | Expected Result |
|------|-------|------------------------|-----------------|
| **0:00 – 1:00** | **1. Dashboard Overview** | Open `http://127.0.0.1:5000/`. Highlight pastel design system, persistent sidebar, and real DB counts. | Stat cards display total book copies, available copies, issued copies, and students. |
| **1:00 – 2:00** | **2. Book Catalogue CRUD & Search** | Navigate to `/books`. Search for "Love hypothesis". Add a new book (e.g., "Clean Architecture", Qty: 2). | Book appears in table with `2 available`. Live search filters properly. |
| **2:00 – 3:00** | **3. Student Registration & Validation** | Navigate to `/students`. Register a new student (ID: `23000999`, Name: `Test Student`, Email: `test@uni.edu`, Dept: `CSE`). | Student registered. Demonstrate duplicate ID rejection if re-entered. |
| **3:00 – 4:30** | **4. Issue Book Workflow** | Navigate to `/issue-return`. Select registered student and "Clean Architecture". Issue book. | Flash message confirms success. Available inventory drops from 2 to 1. Loan appears in Active Loans. |
| **4:30 – 5:30** | **5. Return Book Workflow** | On `/issue-return`, click "📥 Return Book" under Active Loans. | Flash confirms return. Available inventory restores to 2. Active loan list clears. |
| **5:30 – 6:15** | **6. Transactions Log & Deletion Safeguard** | Navigate to `/transactions`. Show logged loan with return date. Navigate to `/books` and show that active loans block book deletion. | Full audit trail visible with badges. Integrity protection demonstrated. |
| **6:15 – 7:15** | **7. Automated Tests & CI Pipeline** | Open Terminal: run `python -m unittest discover -s tests -v`. Open `.github/workflows/tests.yml`. | All 38 tests pass in < 0.5s. Explain Python 3.10/3.12 CI workflow. |
| **7:15 – 8:00** | **8. Jira & Scrum Artifacts** | Open Jira board / review `docs/` artifacts (burndown, sprint plans, retro logs). | Conclude with how user stories and DoD were tracked throughout. |

---

## Pre-Demo Checklist (Run Before Evaluator Joins):
1. **Start Application**:
   ```powershell
   python app.py
   ```
2. **Verify Browser Tab**: Open Chrome or Edge to `http://127.0.0.1:5000/`.
3. **Verify Terminal**: Open a second terminal window in the project folder ready to run `python -m unittest discover -s tests -v`.
4. **Open Documentation**: Have Jira or `docs/` Markdown files open for instant reference.

# Library Book Management System (LBMS)
> **Agile Development using Scrum — Final Semester Evaluation Project**  
> *Developed by a 2-Member Engineering Team · BTech Computer Science & Engineering*

---

## 1. Project Overview & Vision
The **Library Book Management System** is a full-stack academic web platform designed to streamline library cataloging, patron records, and book circulation (issue & return) workflows. Engineered adhering to Agile/Scrum best practices, the system transitions from a rudimentary single-page prototype to a modern multi-page web application featuring a minimalist pastel aesthetic, strict referential data integrity, automated test suites, and CI automation.

---

## 2. Key Features

- **Executive Dashboard**: Real-time statistical cards derived dynamically from SQLite (`Total Books`, `Available Copies`, `Currently Issued`, `Registered Students`), recent transaction activity, and quick-action shortcuts.
- **Book Catalogue & Inventory**: Dedicated collection page with live search (case-insensitive across title and author), book additions, metadata editing, and deletion protections preventing deletion of checked-out books.
- **Student Patron Management**: Comprehensive registration and directory, duplicate ID and email prevention, RFC email format validation, and active loan tracking.
- **Book Circulation (Issue & Return)**:
  - Dropdown selection of registered patrons and available books (`available > 0`).
  - Automated issue date and configurable 14-day loan due dates.
  - Real-time stock decrementing upon issue and restoration upon return.
  - Active loan monitoring with dynamic **Overdue** status flags.
  - Double-return prevention and atomic transaction rollback protection.
- **Circulation History & Auditing**: Filterable transaction log tracking all historical and active loans by status (`All`, `Issued`, `Returned`, `Overdue`).
- **Data Integrity & Security**: Foreign keys enforced via `PRAGMA foreign_keys = ON;`, parameterized SQL queries preventing SQL Injection, and atomic SQLite commits.

---

## 3. Technology Stack

- **Backend**: Python 3.10+, Flask 3.0+
- **Database**: SQLite3 (with foreign key enforcement and atomic transactions)
- **Frontend**: Semantic HTML5, Vanilla CSS3 (custom pastel design system), JavaScript (responsive mobile drawer)
- **Automated Testing**: Python `unittest` (38 automated unit & integration tests), Selenium WebDriver (E2E)
- **CI / DevOps**: GitHub Actions (Multi-version matrix across Python 3.10 and 3.12)
- **Agile / Project Management**: Scrum Framework, Jira Software, Planning Poker, 2-week Sprints

---

## 4. Project Folder Structure

```text
Library_Book_Management_System/
│
├── .github/
│   └── workflows/
│       └── tests.yml                 # GitHub Actions CI workflow
├── docs/                             # Complete Agile/Scrum Documentation
│   ├── product-vision.md             # Vision, goals, scope & DoD
│   ├── product-backlog.md            # Epics, user stories & story points
│   ├── sprint-1-plan.md              # Sprint 1 goals, backlog & tasks
│   ├── sprint-2-plan.md              # Sprint 2 goals, backlog & tasks
│   ├── daily-scrum-template.md       # Standup logs and reusable template
│   ├── sprint-review-retrospective.md# Sprint reviews and retro logs
│   ├── testing-strategy.md           # TDD, test layers & testing quadrants
│   ├── metrics-and-risks.md          # Velocity, burndown & risk register
│   ├── team-responsibilities.md      # 2-person team roles & pair-programming
│   ├── final-report-outline.md       # BTech project report outline
│   ├── jira-setup-guide.md           # Step-by-step Jira setup guide
│   ├── final-demo-checklist.md       # 5-8 minute live viva demo checklist
│   └── solid-principles-and-code-review.md # SOLID & code review guide
├── static/
│   └── style.css                     # Pastel design system & responsive layout
├── templates/
│   ├── base.html                     # Shared layout, persistent sidebar & alerts
│   ├── dashboard.html                # Operational metrics & recent loans
│   ├── books.html                    # Books catalogue, search & add panel
│   ├── edit_book.html                # Book edit view
│   ├── students.html                 # Student directory, search & register panel
│   ├── edit_student.html             # Student edit view
│   ├── issue_return.html             # Issue book form & Active loans return list
│   └── transactions.html             # Full circulation history log & filters
├── tests/
│   ├── test_library_logic.py         # 29 TDD unit tests (in-memory SQLite)
│   ├── test_app.py                   # 9 Flask route integration tests
│   └── test_functional_selenium.py   # Selenium 8-step E2E journey test
├── app.py                            # Flask application routes & controllers
├── database.py                       # SQLite database connection & schema init
├── library_logic.py                  # Domain business logic & validations
├── library.db                        # Production SQLite database (records preserved)
├── requirements.txt                  # Python dependencies
├── .gitignore                        # Git ignore rules
└── README.md                         # Project documentation (this file)
```

---

## 5. Getting Started (Windows Installation & Setup)

### Step 1: Open PowerShell in the Project Directory
```powershell
cd "c:\Users\Shreya\OneDrive\Desktop\semister7\AgileScrum\Final_Project\Library_Book_Management_System_Starter\Library_Book_Management_System"
```

### Step 2: (Optional) Set up Python Virtual Environment
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### Step 3: Install Required Dependencies
```powershell
pip install -r requirements.txt
```

### Step 4: (Optional) Populate Demonstration Data
To populate the database with realistic demonstration Indian students, technical books, and circulation transactions:
```powershell
python seed_demo_data.py
```
*Note: This script is safe and repeatable. It will never overwrite pre-existing data and skips already existing records.*

### Step 5: Run the Application
```powershell
python app.py
```
Open your browser and navigate to:
```text
http://127.0.0.1:5000/
```
*(The root `/` automatically redirects to the operational `/dashboard`)*.

---

## 6. Running Automated Tests

### 1. Execute All Unit and Integration Tests:
Run the comprehensive test discovery runner:
```powershell
python -m unittest discover -s tests -v
```
**Current Test Results**:
- **38 tests passing (100% success rate)** in ~0.3 seconds.
- Tests execute on an isolated temporary/in-memory database, guaranteeing that `library.db` is never modified or polluted by tests.

### 2. Execute Automated Functional UI Tests (Selenium):
```powershell
# Install Selenium and WebDriver manager:
pip install selenium webdriver-manager

# In Terminal 1, ensure Flask is running:
python app.py

# In Terminal 2, run the E2E test runner:
python tests/test_functional_selenium.py
```

---

## 7. GitHub Actions Continuous Integration (CI)

The project includes an automated CI workflow configured in `.github/workflows/tests.yml`.
- **Triggers**: On every `push` and `pull_request` to `main`, `master`, and `develop` branches.
- **Matrix Testing**: Runs on Ubuntu against **Python 3.10** and **Python 3.12**.
- **Automated Verification**: Installs dependencies and executes all unit and integration tests automatically.

---

## 8. Common Errors & Troubleshooting

| Error Message / Issue | Root Cause | Solution |
|-----------------------|------------|----------|
| `TemplateNotFound: dashboard.html` | Flask was searching for `dashboard.html` before template was created. | **Fixed!** Complete template structure (`base.html`, `dashboard.html`, etc.) is now in `templates/`. |
| `Cannot delete book: There are X copy/copies currently issued` | Referential safety lock triggered. | Book cannot be deleted while copies are checked out. Return all copies first. |
| `Student ID or Email already exists` | SQLite unique constraint violated. | Use unique credentials for each student patron. |
| `Selenium WebDriver initialization skipped` | Selenium package not installed locally. | Optional for unit tests. Run `pip install selenium webdriver-manager` if executing E2E UI tests. |

---

## 9. Viva & Evaluation Preparation
For the final 5–8 minute demonstration and viva checklist, please refer to:
- [`docs/final-demo-checklist.md`](docs/final-demo-checklist.md)
- [`docs/jira-setup-guide.md`](docs/jira-setup-guide.md)
- [`docs/solid-principles-and-code-review.md`](docs/solid-principles-and-code-review.md)

# Jira Setup & Configuration Guide for Agile/Scrum Evaluation

This guide provides step-by-step instructions for creating and configuring the Jira project for your academic evaluation. The items below directly reflect the implemented codebase and story breakdown.

---

## 1. Create a New Scrum Project in Jira

1. Log in to [Atlassian Jira](https://www.atlassian.com/software/jira).
2. Click **Projects** -> **Create Project**.
3. Choose the **Scrum** template (under Software Development).
4. Select **Team-managed project** (or Company-managed).
5. Enter:
   - **Project Name**: `Library Book Management System`
   - **Project Key**: `LBMS` (or `LIB`)
6. Click **Create Project**.

---

## 2. Configure Estimation & Board Settings

1. In your project, go to **Project Settings** -> **Features**.
2. Ensure **Backlog**, **Sprints**, and **Reports** are toggled **ON**.
3. Under **Estimation**, set the estimation statistic to **Story Points**.

---

## 3. Create Epics

Go to the **Backlog** view and create the 4 core Epics:
1. `EPIC-1`: **Architectural Foundation & Multi-Page UI Modernization**
   - Color: Purple
   - Summary: Modern multi-page application with pastel theme and sidebar.
2. `EPIC-2`: **Catalogue & Patron Management**
   - Color: Blue
   - Summary: Books and students CRUD with validation and search.
3. `EPIC-3`: **Circulation Management & Data Integrity**
   - Color: Green
   - Summary: Atomic book issue, return, and transaction auditing.
4. `EPIC-4`: **Verification, CI & Scrum Quality Engineering**
   - Color: Orange
   - Summary: TDD unit tests, integration tests, Selenium E2E, and GitHub Actions CI.

---

## 4. Populate User Stories & Tasks into the Backlog

Click **Create Issue** (Issue Type: `Story`) and assign to their respective Epics:

| Issue Key | Summary | Story Points | Priority | Epic Link | Assignee |
|-----------|---------|--------------|----------|-----------|----------|
| **LBMS-1** | As a Librarian, I want global navigation and a pastel design system | 5 | Highest | EPIC-1 | Member 2 |
| **LBMS-2** | As an Admin, I want an operational metrics dashboard | 3 | High | EPIC-1 | Member 1 |
| **LBMS-3** | As a Librarian, I want book catalogue CRUD and search | 5 | High | EPIC-2 | Member 1 |
| **LBMS-4** | As a Librarian, I want student registration and directory | 5 | High | EPIC-2 | Member 2 |
| **LBMS-5** | As a Librarian, I want an atomic book issue workflow | 8 | Highest | EPIC-3 | Member 1 |
| **LBMS-6** | As a Librarian, I want a book return workflow with inventory updates | 5 | High | EPIC-3 | Member 1 |
| **LBMS-7** | As an Auditor, I want a circulation history and filterable log | 3 | Medium | EPIC-3 | Member 2 |
| **LBMS-8** | As an Evaluator, I want TDD unit & Flask integration tests | 5 | Highest | EPIC-4 | Member 2 |
| **LBMS-9** | As a QA Engineer, I want an automated functional Selenium test suite | 3 | Medium | EPIC-4 | Member 2 |
| **LBMS-10**| As a Developer, I want GitHub Actions CI running tests on push/PR | 2 | High | EPIC-4 | Member 2 |

*Tip: For each story, paste the Acceptance Criteria from `docs/product-backlog.md` into the Description field.*

---

## 5. Plan and Start Sprints

### Setting up Sprint 1:
1. Click **Create Sprint** at the top of the Backlog. Name it: `Sprint 1 - Foundation & Catalogue`.
2. Duration: 2 weeks.
3. Drag the following stories into Sprint 1:
   - `LBMS-1` (5 pts)
   - `LBMS-2` (3 pts)
   - `LBMS-3` (5 pts)
   - `LBMS-4` (5 pts)
   - *Total Sprint 1 Commitment: 18 Story Points*.
4. Click **Start Sprint**.

### Setting up Sprint 2:
1. Click **Create Sprint**. Name it: `Sprint 2 - Circulation, Testing & CI`.
2. Duration: 2 weeks.
3. Drag remaining stories into Sprint 2:
   - `LBMS-5` (8 pts)
   - `LBMS-6` (5 pts)
   - `LBMS-7` (3 pts)
   - `LBMS-8` (5 pts)
   - `LBMS-9` (3 pts)
   - `LBMS-10` (2 pts)
   - *Total Sprint 2 Commitment: 26 Story Points*.

---

## 6. Daily Scrum & Workflow Progress Simulation

During the sprint:
- Move tickets from `To Do` -> `In Progress` -> `In Review` -> `Done`.
- In sub-tasks, log work (e.g. `Log Work -> 3h`).
- When all tickets in Sprint 1 are moved to `Done`, click **Complete Sprint**.
- Start Sprint 2, progress tickets across the board, and complete Sprint 2.

---

## 7. Generating Burndown & Velocity Evidence for Evaluation

1. Go to **Reports** in the left navigation sidebar.
2. Select **Burndown Chart** -> Choose `Sprint 1` and `Sprint 2`.
3. Take screenshots showing the burning down of story points.
4. Select **Velocity Chart** showing:
   - Sprint 1: 18 committed, 18 completed.
   - Sprint 2: 26 committed, 26 completed.
5. Save screenshots into your project report or presentation deck.

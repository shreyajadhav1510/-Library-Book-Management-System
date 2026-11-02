# Metrics, Velocity & Risk Management

## 1. Velocity & Sprint Performance Metrics

In Scrum, **Velocity** measures the amount of work (in Story Points) a Development Team successfully completes per Sprint according to the Definition of Done.

### Historical Sprint Metrics Table

| Sprint | Committed Points | Completed (Done) Points | Planned Velocity | Actual Velocity | Defect Leakage | Test Pass Rate |
|--------|------------------|-------------------------|------------------|-----------------|----------------|----------------|
| **Sprint 1** | 18 | 18 | 18 | 18 | 0 | 100% |
| **Sprint 2** | 26 | 26 | 24 | 26 | 0 | 100% |
| **Total** | **44** | **44** | — | **Avg: 22 pts/sprint** | **0** | **100%** |

---

## 2. Sprint Burndown Chart Guidelines

A **Sprint Burndown Chart** plots remaining story points day-by-day across the sprint timeline against an ideal linear burndown trajectory.

### Sprint 1 Burndown Profile (10 Working Days, 18 Points):
- **Day 0**: 18 pts remaining (Sprint Start)
- **Day 2**: 15 pts remaining (US-102 completed)
- **Day 4**: 10 pts remaining (US-101 completed)
- **Day 7**: 5 pts remaining (US-201 completed)
- **Day 10**: 0 pts remaining (US-202 completed, Sprint 1 Done)

### Sprint 2 Burndown Profile (10 Working Days, 26 Points):
- **Day 0**: 26 pts remaining
- **Day 3**: 18 pts remaining (US-301 completed)
- **Day 5**: 13 pts remaining (US-302 completed)
- **Day 7**: 10 pts remaining (US-303 completed)
- **Day 8**: 5 pts remaining (US-401 completed)
- **Day 10**: 0 pts remaining (US-402, US-403 completed, All Criteria Done)

### Generating Burndown in Jira:
1. Navigate to **Jira Software** -> Select Project -> **Reports** in sidebar.
2. Click **Burndown Chart**.
3. Select `Sprint 1` or `Sprint 2` from the drop-down.
4. Export chart image or embed screenshot in the final presentation.

---

## 3. Project Risk Register & Mitigation Strategy

| Risk ID | Risk Description | Category | Severity | Probability | Impact Score | Mitigation Strategy & Contingency | Status |
|---------|------------------|----------|----------|-------------|--------------|-----------------------------------|--------|
| **RSK-01** | **Data Loss / SQLite Corruption**: Overwriting existing database file destroys pre-existing book records. | Technical | Critical | High | High | Enforced strict `.gitignore` rules; implemented `init_db()` using `CREATE TABLE IF NOT EXISTS`; automated pre-edit checks. | **Mitigated** |
| **RSK-02** | **Referential Orphan Records**: Deleting a book or student while actively borrowed corrupts audit history. | Data Integrity | High | Medium | High | Added SQL Foreign Key constraints (`PRAGMA foreign_keys = ON`) and programmatic deletion locks in `library_logic.py`. | **Mitigated** |
| **RSK-03** | **Concurrent Loan Race Condition**: Two users issuing the last copy simultaneously causing negative inventory. | Concurrency | High | Low | Medium | Wrapped loan updates in atomic SQLite transactions; validated `available > 0` directly before execution. | **Mitigated** |
| **RSK-04** | **CI Environment Failure**: WebDriver missing in headless container causes build break. | DevOps | Medium | High | Medium | Built headless fallbacks and separated Selenium functional tests from blocking unit tests. | **Mitigated** |
| **RSK-05** | **Scope Creep / Gold-Plating**: Adding RFID/SMS features jeopardizes sprint deadline. | Process | Medium | Medium | Medium | Scrum Master strictly enforced Sprint Backlog scope using MoSCoW prioritization. | **Mitigated** |

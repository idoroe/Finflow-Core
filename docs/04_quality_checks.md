# Data Quality Checks

## Philosophy

Every check is a SQL query that returns **failing rows**. If the query returns 0 rows, the check PASSES. Any rows = FAIL.

## Checks Implemented

| # | Check | What it catches |
|---|-------|----------------|
| 1 | DIM_CUSTOMER NULL PK | Customers loaded without an ID |
| 2 | DIM_ACCOUNT NULL PK | Accounts loaded without an ID |
| 3 | FCT_TRANSACTIONS NULL PK | Transactions loaded without an ID |
| 4 | DIM_CUSTOMER DUPLICATE PK | Same customer loaded twice |
| 5 | FCT_TRANSACTIONS DUPLICATE PK | Same transaction loaded twice |
| 6 | ORPHAN TRANSACTIONS | Transactions referencing non-existent accounts |
| 7 | MISSING DATES | Transactions with dates not in DIM_DATE |
| 8 | NEGATIVE AMOUNTS | Transactions with negative amounts (may or may not be valid depending on business rules) |

## How the Pipeline Uses Checks

- If ANY check fails, the pipeline **stops** and logs which checks failed
- This prevents downstream consumers from using bad data
- Check results are logged with timestamps for debugging

---

**TODO**: Add more checks as you discover data issues during development.

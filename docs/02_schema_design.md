# Schema Design

## Business Process

We are modeling **banking transactions** — the flow of money in and out of customer accounts.

## Grain

**One row per transaction.** Each row in `FCT_TRANSACTIONS` represents a single banking transaction (deposit, withdrawal, payment, etc.).

## Star Schema

```
                    DIM_DATE
                       |
DIM_CUSTOMER --- FCT_TRANSACTIONS --- DIM_ACCOUNT
                       |
                  DIM_DISTRICT
```

## Dimension Tables

| Table | Primary Key | Purpose |
|-------|-------------|---------|
| DIM_DATE | DATE_KEY | Calendar attributes (year, month, quarter, day of week) |
| DIM_CUSTOMER | CUSTOMER_KEY | Customer demographics (gender, birth date, location) |
| DIM_ACCOUNT | ACCOUNT_KEY | Account attributes (frequency, open date, district) |
| DIM_DISTRICT | DISTRICT_KEY | Geographic info (region, population, avg salary) |

## Fact Table

| Table | Primary Key | Measures |
|-------|-------------|----------|
| FCT_TRANSACTIONS | TRANSACTION_KEY | AMOUNT, BALANCE |

## Design Tradeoffs

1. **Surrogate keys vs natural keys**: We use natural keys (original IDs from the source) for simplicity. In production, you'd generate integer surrogate keys for better join performance.

2. **Truncate+Insert vs MERGE**: We chose truncate+insert for idempotency because our dataset is small. For tables with millions of rows, MERGE (upsert) would be more efficient.

3. **Date dimension**: We generate DIM_DATE from transaction dates only. In production, you'd pre-populate a full calendar (e.g., 2000-2030).

4. **DIM_DISTRICT from coded columns**: The source district data uses generic column names (A1–A16). We rename them to meaningful names (POPULATION, AVG_SALARY, etc.) during the transform step, so ANALYTICS queries are self-documenting.

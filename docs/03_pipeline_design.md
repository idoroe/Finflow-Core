# Pipeline Design

## Run Order

The pipeline executes in this exact order every time:

1. **Config check** — Verify Snowflake credentials are set
2. **Snowflake setup** — Create database, schemas, warehouse (if not exists)
3. **Create RAW tables** — DDL for staging tables
4. **Load RAW data** — CSV files → Snowflake RAW tables
5. **Create ANALYTICS tables** — DDL for star schema
6. **Transform RAW → ANALYTICS** — SQL transformations (truncate + insert)
7. **Quality checks** — Validate data integrity
8. **Demo queries + benchmarks** — Run analytics queries and measure timing

## Idempotency Strategy

**Approach: Truncate + Insert**

Every run:
- RAW tables: `overwrite=True` in `write_pandas()` wipes and reloads
- ANALYTICS tables: `TRUNCATE TABLE` then `INSERT INTO` rebuilds from scratch

This means you can safely run the pipeline 100 times and always get the same result.

## Failure Modes

| Failure | What happens | How to fix |
|---------|-------------|------------|
| Missing .env | Pipeline stops at step 1 with clear error | Copy .env.example to .env and fill in credentials |
| Snowflake connection fails | Pipeline stops with connection error | Check credentials, account identifier, network |
| CSV file missing | Warning logged, pipeline continues | Add CSV files to data/ directory |
| Quality check fails | Pipeline stops at step 7 | Investigate failing check in logs, fix SQL or data |

## How to Run

```bash
python -m src.run_all
```

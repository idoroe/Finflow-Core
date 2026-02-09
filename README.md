# FinFlow Core

A Python + Snowflake data warehouse pipeline that loads raw banking data, transforms it into a star schema, runs automated quality checks, and produces analytics queries with measured performance optimizations.

## Architecture

```
Raw CSVs (8 files, 1M+ rows)
        |
        v
Python Loader (batch INSERT)
        |
        v
Snowflake RAW schema (8 staging tables, all VARCHAR)
        |
        v
SQL Transforms (type casting, cleaning, decoding)
        |
        v
Snowflake ANALYTICS schema (star schema: 4 dim + 1 fct)
        |
        v
Quality Checks (8 automated checks) + Demo Queries (6 analytics queries)
```

## Star Schema

```
                DIM_DATE (2,191 rows)
                    |
DIM_CUSTOMER ---  FCT_TRANSACTIONS (1,056,320 rows)  --- DIM_ACCOUNT
  (5,369)           |                                      (4,500)
                DIM_DISTRICT (71 rows)
```

## Quick Start

```bash
# 1. Clone and set up virtual environment
git clone <repo-url>
cd Finflow-Core
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Configure Snowflake credentials
cp .env.example .env
# Edit .env with your Snowflake account, username, and password

# 3. Run the full pipeline
python -m src.run_all
```

## Project Structure

```
sql/                          # SQL scripts (run in order)
  00_setup_snowflake.sql      # Create database, schemas, warehouse
  01_create_raw_tables.sql    # Create 8 RAW staging tables
  02_create_analytics_tables.sql  # Create star schema (dim + fct)
  03_transform_raw_to_analytics.sql  # Transform RAW -> ANALYTICS
  04_quality_checks.sql       # 8 data quality checks
  05_demo_queries.sql         # 6 analytics queries

src/                          # Python pipeline code
  run_all.py                  # Main entry point — runs everything
  config.py                   # Loads .env credentials
  logging_config.py           # Structured logging setup
  load/snowflake_client.py    # Snowflake connection wrapper
  load/load_raw.py            # CSV -> Snowflake RAW loader
  transform/build_analytics.py  # Runs transform SQL
  validate/run_quality_checks.py  # Runs quality check SQL
  perf/run_benchmarks.py      # Times demo queries

tests/                        # pytest test suite
docs/                         # Project documentation
data/                         # CSV data files (not committed)
```

## Dataset

Czech Banking Dataset (8 semicolon-delimited CSV files):
- **trans.csv** (1,056,320 rows) — banking transactions
- **account.csv** (4,500) — bank accounts
- **client.csv** (5,369) — customers
- **disp.csv** (5,369) — client-account relationships
- **order.csv** (6,471) — standing orders
- **card.csv** (892) — bank cards
- **loan.csv** (682) — loans
- **district.csv** (77) — geographic regions

## Performance Results

| Query | Before Clustering | After Clustering (YEAR+MONTH) | Improvement |
|-------|------------------|-------------------------------|-------------|
| Monthly volume | 949ms | 312ms | 67% faster |
| Top 10 accounts | 546ms | 231ms | 58% faster |
| Date range filter | 80ms | 101ms | ~same |

See [docs/05_performance.md](docs/05_performance.md) for full analysis.

## Documentation

- [Overview](docs/00_overview.md)
- [Data Dictionary](docs/01_data_dictionary.md)
- [Schema Design](docs/02_schema_design.md)
- [Pipeline Design](docs/03_pipeline_design.md)
- [Quality Checks](docs/04_quality_checks.md)
- [Performance](docs/05_performance.md)
- [Demo Questions](docs/06_demo_questions.md)

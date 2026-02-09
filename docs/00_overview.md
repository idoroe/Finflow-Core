# FinFlow Core — Overview

## What is this?

FinFlow Core is a Python + Snowflake data pipeline that simulates what enterprise data teams (like the one at RBC) build daily.

## Architecture

```
Raw CSVs → Python Loader → Snowflake RAW schema → SQL Transforms → Snowflake ANALYTICS schema (star schema) → Quality Checks → Demo Queries
```

## Key Technologies

| Tool | What it does | Why we use it |
|------|-------------|---------------|
| Python | Orchestrates the pipeline | Industry standard for data engineering |
| Snowflake | Cloud data warehouse | Stores and queries all our data |
| SQL | Data transformations | The language of data |
| pandas | Reads CSV files | Fast and reliable for file I/O |
| pytest | Runs tests | Catches bugs before they hit production |

## How to Run

```bash
# 1. Activate virtual environment
source venv/bin/activate

# 2. Set up your .env file with Snowflake credentials
cp .env.example .env
# Edit .env with your Snowflake account details

# 3. Run the full pipeline
python -m src.run_all
```

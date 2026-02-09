# Performance Notes

## Baseline Measurements (No Clustering)

| Query | Description | Duration |
|-------|------------|----------|
| RAW data load | Python batch INSERT (8 CSVs, 1M+ rows) | ~22 min |
| Query 1 | Monthly transaction volume (JOIN + GROUP BY) | 949ms |
| Query 2 | Top 10 accounts (2 JOINs + GROUP BY + ORDER BY) | 546ms |
| Query 3 | Date range filter (WHERE on 1 year) | 80ms |

## Optimization 1: Clustering by TRANSACTION_DATE

**What we did:** `ALTER TABLE FCT_TRANSACTIONS CLUSTER BY (TRANSACTION_DATE)`

**Result:** Queries 1 and 2 improved significantly, but Snowflake warned about high cardinality (2,191 unique dates = too many partition boundaries). Query 3 got slightly worse because the clustering metadata overhead exceeded the scan time for an already-fast query.

| Query | Before | After | Change |
|-------|--------|-------|--------|
| Query 1 | 949ms | 318ms | **66% faster** |
| Query 2 | 546ms | 179ms | **67% faster** |
| Query 3 | 80ms | 106ms | 33% slower |

**Lesson learned:** High-cardinality clustering keys are expensive to maintain. Use lower-cardinality alternatives.

## Optimization 2: Clustering by YEAR + MONTH (Final)

**What we did:** Dropped the date clustering key and replaced with:
`ALTER TABLE FCT_TRANSACTIONS CLUSTER BY (YEAR(TRANSACTION_DATE), MONTH(TRANSACTION_DATE))`

**Why:** YEAR has 6 unique values, MONTH has 12 — combined ~72 combinations vs 2,191 dates. Much cheaper for Snowflake to maintain and still enables effective partition pruning for date-range queries.

| Query | Baseline | After Optimization | Improvement |
|-------|----------|-------------------|-------------|
| Query 1 (Monthly volume) | 949ms | 312ms | **67% faster** |
| Query 2 (Top 10 accounts) | 546ms | 231ms | **58% faster** |
| Query 3 (Date range filter) | 80ms | 101ms | ~same (within noise) |

## Key Takeaways

1. **Clustering keys improve queries that filter or group by the clustered columns.** Our monthly aggregation (Query 1) improved 67% because data is now physically organized by year+month.

2. **Avoid high-cardinality clustering keys.** Clustering on exact dates (2,191 values) caused expensive re-clustering. Clustering on YEAR+MONTH (72 values) achieved similar performance with lower maintenance cost.

3. **Very fast queries may not benefit from clustering.** Query 3 was already 80ms — at that speed, the overhead of checking clustering metadata can exceed the benefit.

4. **Always measure before and after.** Never assume an optimization helps — prove it with numbers.

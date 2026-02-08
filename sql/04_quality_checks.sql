-- 04_quality_checks.sql
-- Data quality checks. Each query should return 0 rows if the check PASSES.
-- Any rows returned = a problem that needs investigation.
--
-- HIGH-LEVEL EXPLANATION:
--   These are automated "tests" for your data. Just like unit tests check
--   your code, quality checks verify your data is correct.
--
--   Pattern: SELECT rows WHERE something_is_wrong
--   If result is empty -> PASS
--   If result has rows  -> FAIL (those rows have problems)

USE DATABASE FINFLOW;
USE SCHEMA ANALYTICS;

-- Check 1: No NULL primary keys in DIM_CUSTOMER
SELECT 'DIM_CUSTOMER NULL PK' AS CHECK_NAME, CUSTOMER_KEY
FROM DIM_CUSTOMER
WHERE CUSTOMER_KEY IS NULL;

-- Check 2: No NULL primary keys in DIM_ACCOUNT
SELECT 'DIM_ACCOUNT NULL PK' AS CHECK_NAME, ACCOUNT_KEY
FROM DIM_ACCOUNT
WHERE ACCOUNT_KEY IS NULL;

-- Check 3: No NULL primary keys in FCT_TRANSACTIONS
SELECT 'FCT_TRANSACTIONS NULL PK' AS CHECK_NAME, TRANSACTION_KEY
FROM FCT_TRANSACTIONS
WHERE TRANSACTION_KEY IS NULL;

-- Check 4: No duplicate primary keys in DIM_CUSTOMER
SELECT 'DIM_CUSTOMER DUPLICATE PK' AS CHECK_NAME, CUSTOMER_KEY, COUNT(*) AS CNT
FROM DIM_CUSTOMER
GROUP BY CUSTOMER_KEY
HAVING COUNT(*) > 1;

-- Check 5: No duplicate primary keys in FCT_TRANSACTIONS
SELECT 'FCT_TRANSACTIONS DUPLICATE PK' AS CHECK_NAME, TRANSACTION_KEY, COUNT(*) AS CNT
FROM FCT_TRANSACTIONS
GROUP BY TRANSACTION_KEY
HAVING COUNT(*) > 1;

-- Check 6: Referential integrity — every transaction should reference an existing account
SELECT 'ORPHAN TRANSACTIONS' AS CHECK_NAME, f.TRANSACTION_KEY, f.ACCOUNT_KEY
FROM FCT_TRANSACTIONS f
LEFT JOIN DIM_ACCOUNT a ON f.ACCOUNT_KEY = a.ACCOUNT_KEY
WHERE a.ACCOUNT_KEY IS NULL;

-- Check 7: Transaction dates should exist in DIM_DATE
SELECT 'MISSING DATES' AS CHECK_NAME, f.TRANSACTION_KEY, f.TRANSACTION_DATE
FROM FCT_TRANSACTIONS f
LEFT JOIN DIM_DATE d ON f.TRANSACTION_DATE = d.DATE_KEY
WHERE d.DATE_KEY IS NULL;

-- Check 8: Transaction amounts should be positive
SELECT 'NEGATIVE AMOUNTS' AS CHECK_NAME, TRANSACTION_KEY, AMOUNT
FROM FCT_TRANSACTIONS
WHERE AMOUNT < 0

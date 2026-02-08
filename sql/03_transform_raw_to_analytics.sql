-- 03_transform_raw_to_analytics.sql
-- Transforms RAW data into the ANALYTICS star schema tables.
--
-- HIGH-LEVEL EXPLANATION:
--   This is where the "business logic" lives. We:
--     1. Read from RAW tables (messy VARCHAR data)
--     2. Cast columns to proper types (VARCHAR -> INT, DATE, DECIMAL)
--     3. Clean up values (trim whitespace, handle NULLs)
--     4. Insert into ANALYTICS tables
--
--   IDEMPOTENCY: We use TRUNCATE + INSERT, meaning every run wipes the
--   analytics tables and reloads from scratch. This is the simplest approach
--   and guarantees consistency. For larger datasets, you'd use MERGE (upsert).
--
-- WHY TRUNCATE + INSERT?
--   It's simple, predictable, and safe. If something goes wrong, just re-run.
--   The tradeoff is that it's slower for huge tables (millions of rows),
--   but for our dataset size it's perfectly fine.

USE DATABASE FINFLOW;

-- ============================================
-- Populate DIM_DATE
-- Generate a date dimension from the transaction dates
-- ============================================
TRUNCATE TABLE ANALYTICS.DIM_DATE;

INSERT INTO ANALYTICS.DIM_DATE (DATE_KEY, YEAR, MONTH, DAY, DAY_OF_WEEK, MONTH_NAME, QUARTER)
SELECT DISTINCT
    TRY_TO_DATE(t.DATE, 'YYYYMMDD')                    AS DATE_KEY,
    YEAR(TRY_TO_DATE(t.DATE, 'YYYYMMDD'))               AS YEAR,
    MONTH(TRY_TO_DATE(t.DATE, 'YYYYMMDD'))              AS MONTH,
    DAY(TRY_TO_DATE(t.DATE, 'YYYYMMDD'))                AS DAY,
    DAYOFWEEK(TRY_TO_DATE(t.DATE, 'YYYYMMDD'))          AS DAY_OF_WEEK,
    MONTHNAME(TRY_TO_DATE(t.DATE, 'YYYYMMDD'))          AS MONTH_NAME,
    QUARTER(TRY_TO_DATE(t.DATE, 'YYYYMMDD'))            AS QUARTER
FROM RAW.TRANSACTIONS t
WHERE TRY_TO_DATE(t.DATE, 'YYYYMMDD') IS NOT NULL;

-- ============================================
-- Populate DIM_CUSTOMER
-- ============================================
TRUNCATE TABLE ANALYTICS.DIM_CUSTOMER;

INSERT INTO ANALYTICS.DIM_CUSTOMER (CUSTOMER_KEY, BIRTH_DATE, GENDER, DISTRICT_ID)
SELECT
    TRY_TO_NUMBER(c.CLIENT_ID)                          AS CUSTOMER_KEY,
    TRY_TO_DATE(c.BIRTH_DATE, 'YYYYMMDD')              AS BIRTH_DATE,
    TRIM(c.GENDER)                                       AS GENDER,
    TRY_TO_NUMBER(c.DISTRICT_ID)                         AS DISTRICT_ID
FROM RAW.CLIENTS c
WHERE TRY_TO_NUMBER(c.CLIENT_ID) IS NOT NULL;

-- ============================================
-- Populate DIM_ACCOUNT
-- ============================================
TRUNCATE TABLE ANALYTICS.DIM_ACCOUNT;

INSERT INTO ANALYTICS.DIM_ACCOUNT (ACCOUNT_KEY, DISTRICT_ID, FREQUENCY, OPEN_DATE)
SELECT
    TRY_TO_NUMBER(a.ACCOUNT_ID)                          AS ACCOUNT_KEY,
    TRY_TO_NUMBER(a.DISTRICT_ID)                         AS DISTRICT_ID,
    TRIM(a.FREQUENCY)                                     AS FREQUENCY,
    TRY_TO_DATE(a.DATE, 'YYYYMMDD')                      AS OPEN_DATE
FROM RAW.ACCOUNTS a
WHERE TRY_TO_NUMBER(a.ACCOUNT_ID) IS NOT NULL;

-- ============================================
-- Populate DIM_DISTRICT
-- ============================================
TRUNCATE TABLE ANALYTICS.DIM_DISTRICT;

INSERT INTO ANALYTICS.DIM_DISTRICT (DISTRICT_KEY, DISTRICT_NAME, REGION, POPULATION, AVG_SALARY)
SELECT
    TRY_TO_NUMBER(d.DISTRICT_ID)                         AS DISTRICT_KEY,
    TRIM(d.DISTRICT_NAME)                                 AS DISTRICT_NAME,
    TRIM(d.REGION)                                        AS REGION,
    TRY_TO_NUMBER(d.POPULATION)                           AS POPULATION,
    TRY_TO_DECIMAL(d.AVG_SALARY, 12, 2)                   AS AVG_SALARY
FROM RAW.DISTRICTS d
WHERE TRY_TO_NUMBER(d.DISTRICT_ID) IS NOT NULL;

-- ============================================
-- Populate FCT_TRANSACTIONS (the core fact table)
-- ============================================
TRUNCATE TABLE ANALYTICS.FCT_TRANSACTIONS;

INSERT INTO ANALYTICS.FCT_TRANSACTIONS (
    TRANSACTION_KEY, ACCOUNT_KEY, TRANSACTION_DATE,
    TYPE, OPERATION, AMOUNT, BALANCE, K_SYMBOL
)
SELECT
    TRY_TO_NUMBER(t.TRANS_ID)                            AS TRANSACTION_KEY,
    TRY_TO_NUMBER(t.ACCOUNT_ID)                          AS ACCOUNT_KEY,
    TRY_TO_DATE(t.DATE, 'YYYYMMDD')                      AS TRANSACTION_DATE,
    TRIM(t.TYPE)                                          AS TYPE,
    TRIM(t.OPERATION)                                     AS OPERATION,
    TRY_TO_DECIMAL(t.AMOUNT, 12, 2)                       AS AMOUNT,
    TRY_TO_DECIMAL(t.BALANCE, 12, 2)                      AS BALANCE,
    TRIM(t.K_SYMBOL)                                      AS K_SYMBOL
FROM RAW.TRANSACTIONS t
WHERE TRY_TO_NUMBER(t.TRANS_ID) IS NOT NULL

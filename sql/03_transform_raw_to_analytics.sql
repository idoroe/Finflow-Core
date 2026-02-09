-- 03_transform_raw_to_analytics.sql
-- Transforms RAW data into the ANALYTICS star schema tables.
--
-- HIGH-LEVEL EXPLANATION:
--   This is where the "business logic" lives. Key transformations:
--     1. Dates in YYMMDD format (like 930101) get converted to proper dates
--     2. The birth_number field gets decoded into birth_date + gender
--        (if month > 12, the person is female and we subtract 50 from month)
--     3. District columns A1-A16 get renamed to meaningful names
--     4. All text is trimmed, numbers are cast to proper types
--
--   IDEMPOTENCY: TRUNCATE + INSERT — wipe and reload every run.

USE DATABASE FINFLOW;

-- ============================================
-- Populate DIM_DATE
-- Generate a date dimension from the transaction dates
-- Czech dataset uses YYMMDD format (6 digits like 930101)
-- We need to prepend century: 93 -> 1993
-- ============================================
TRUNCATE TABLE ANALYTICS.DIM_DATE;

INSERT INTO ANALYTICS.DIM_DATE (DATE_KEY, YEAR, MONTH, DAY, DAY_OF_WEEK, MONTH_NAME, QUARTER)
SELECT DISTINCT
    TRY_TO_DATE(LPAD(t.DATE, 6, '0'), 'YYMMDD')          AS DATE_KEY,
    YEAR(TRY_TO_DATE(LPAD(t.DATE, 6, '0'), 'YYMMDD'))     AS YEAR,
    MONTH(TRY_TO_DATE(LPAD(t.DATE, 6, '0'), 'YYMMDD'))    AS MONTH,
    DAY(TRY_TO_DATE(LPAD(t.DATE, 6, '0'), 'YYMMDD'))      AS DAY,
    DAYOFWEEK(TRY_TO_DATE(LPAD(t.DATE, 6, '0'), 'YYMMDD')) AS DAY_OF_WEEK,
    MONTHNAME(TRY_TO_DATE(LPAD(t.DATE, 6, '0'), 'YYMMDD')) AS MONTH_NAME,
    QUARTER(TRY_TO_DATE(LPAD(t.DATE, 6, '0'), 'YYMMDD'))  AS QUARTER
FROM RAW.TRANS t
WHERE TRY_TO_DATE(LPAD(t.DATE, 6, '0'), 'YYMMDD') IS NOT NULL;

-- ============================================
-- Populate DIM_CUSTOMER
-- Decode birth_number: YYMMDD format
--   If month > 12, the client is female (subtract 50 from month)
--   e.g., 706213 -> YY=70, MM=62(female, real month=12), DD=13
-- ============================================
TRUNCATE TABLE ANALYTICS.DIM_CUSTOMER;

INSERT INTO ANALYTICS.DIM_CUSTOMER (CUSTOMER_KEY, BIRTH_DATE, GENDER, DISTRICT_ID)
SELECT
    TRY_TO_NUMBER(c.CLIENT_ID)                              AS CUSTOMER_KEY,
    TRY_TO_DATE(
        LPAD(SUBSTR(c.BIRTH_NUMBER, 1, 2), 2, '0')
        || LPAD(
            CASE
                WHEN TRY_TO_NUMBER(SUBSTR(c.BIRTH_NUMBER, 3, 2)) > 50
                THEN TRY_TO_NUMBER(SUBSTR(c.BIRTH_NUMBER, 3, 2)) - 50
                ELSE TRY_TO_NUMBER(SUBSTR(c.BIRTH_NUMBER, 3, 2))
            END, 2, '0')
        || SUBSTR(c.BIRTH_NUMBER, 5, 2),
        'YYMMDD'
    )                                                        AS BIRTH_DATE,
    CASE
        WHEN TRY_TO_NUMBER(SUBSTR(c.BIRTH_NUMBER, 3, 2)) > 50 THEN 'Female'
        ELSE 'Male'
    END                                                      AS GENDER,
    TRY_TO_NUMBER(c.DISTRICT_ID)                             AS DISTRICT_ID
FROM RAW.CLIENT c
WHERE TRY_TO_NUMBER(c.CLIENT_ID) IS NOT NULL;

-- ============================================
-- Populate DIM_ACCOUNT
-- ============================================
TRUNCATE TABLE ANALYTICS.DIM_ACCOUNT;

INSERT INTO ANALYTICS.DIM_ACCOUNT (ACCOUNT_KEY, DISTRICT_ID, FREQUENCY, OPEN_DATE)
SELECT
    TRY_TO_NUMBER(a.ACCOUNT_ID)                              AS ACCOUNT_KEY,
    TRY_TO_NUMBER(a.DISTRICT_ID)                             AS DISTRICT_ID,
    TRIM(a.FREQUENCY)                                         AS FREQUENCY,
    TRY_TO_DATE(LPAD(a.DATE, 6, '0'), 'YYMMDD')              AS OPEN_DATE
FROM RAW.ACCOUNT a
WHERE TRY_TO_NUMBER(a.ACCOUNT_ID) IS NOT NULL;

-- ============================================
-- Populate DIM_DISTRICT
-- Rename A1-A16 to meaningful column names
-- A1=district_id, A2=name, A3=region, A4=population,
-- A5=municipalities<499, A6=municipalities 500-1999,
-- A7=municipalities 2000-9999, A8=num cities,
-- A9=urban ratio, A10=avg salary (not used: A11=unemployment95,
-- A12=unemployment96, A13=entrepreneurs, A14=crimes95, A15=crimes96, A16=not used)
-- ============================================
TRUNCATE TABLE ANALYTICS.DIM_DISTRICT;

INSERT INTO ANALYTICS.DIM_DISTRICT (
    DISTRICT_KEY, DISTRICT_NAME, REGION, POPULATION,
    NUM_MUNICIPALITIES_LT_499, NUM_MUNICIPALITIES_500_1999,
    NUM_MUNICIPALITIES_2000_9999, NUM_CITIES,
    URBAN_RATIO, AVG_SALARY,
    UNEMPLOYMENT_95, UNEMPLOYMENT_96,
    NUM_ENTREPRENEURS, NUM_CRIMES_95, NUM_CRIMES_96
)
SELECT
    TRY_TO_NUMBER(d.A1)                                      AS DISTRICT_KEY,
    TRIM(d.A2)                                                AS DISTRICT_NAME,
    TRIM(d.A3)                                                AS REGION,
    TRY_TO_NUMBER(d.A4)                                      AS POPULATION,
    TRY_TO_NUMBER(d.A5)                                      AS NUM_MUNICIPALITIES_LT_499,
    TRY_TO_NUMBER(d.A6)                                      AS NUM_MUNICIPALITIES_500_1999,
    TRY_TO_NUMBER(d.A7)                                      AS NUM_MUNICIPALITIES_2000_9999,
    TRY_TO_NUMBER(d.A8)                                      AS NUM_CITIES,
    TRY_TO_DECIMAL(d.A9, 5, 1)                                AS URBAN_RATIO,
    TRY_TO_NUMBER(d.A10)                                     AS AVG_SALARY,
    TRY_TO_DECIMAL(d.A11, 5, 2)                               AS UNEMPLOYMENT_95,
    TRY_TO_DECIMAL(d.A12, 5, 2)                               AS UNEMPLOYMENT_96,
    TRY_TO_NUMBER(d.A13)                                     AS NUM_ENTREPRENEURS,
    TRY_TO_NUMBER(d.A14)                                     AS NUM_CRIMES_95,
    TRY_TO_NUMBER(d.A15)                                     AS NUM_CRIMES_96
FROM RAW.DISTRICT d
WHERE TRY_TO_NUMBER(d.A1) IS NOT NULL;

-- ============================================
-- Populate FCT_TRANSACTIONS (the core fact table)
-- ============================================
TRUNCATE TABLE ANALYTICS.FCT_TRANSACTIONS;

INSERT INTO ANALYTICS.FCT_TRANSACTIONS (
    TRANSACTION_KEY, ACCOUNT_KEY, TRANSACTION_DATE,
    TYPE, OPERATION, AMOUNT, BALANCE, K_SYMBOL
)
SELECT
    TRY_TO_NUMBER(t.TRANS_ID)                                AS TRANSACTION_KEY,
    TRY_TO_NUMBER(t.ACCOUNT_ID)                              AS ACCOUNT_KEY,
    TRY_TO_DATE(LPAD(t.DATE, 6, '0'), 'YYMMDD')              AS TRANSACTION_DATE,
    TRIM(t.TYPE)                                              AS TYPE,
    TRIM(t.OPERATION)                                         AS OPERATION,
    TRY_TO_DECIMAL(t.AMOUNT, 12, 2)                           AS AMOUNT,
    TRY_TO_DECIMAL(t.BALANCE, 12, 2)                          AS BALANCE,
    TRIM(t.K_SYMBOL)                                          AS K_SYMBOL
FROM RAW.TRANS t
WHERE TRY_TO_NUMBER(t.TRANS_ID) IS NOT NULL

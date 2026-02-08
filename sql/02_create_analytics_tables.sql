-- 02_create_analytics_tables.sql
-- Creates the star schema tables in the ANALYTICS schema.
--
-- HIGH-LEVEL EXPLANATION:
--   This is the STAR SCHEMA — the clean, analytics-ready layer.
--
--   DIMENSION tables (dim_): describe WHO, WHAT, WHERE, WHEN
--     - dim_customer: who is the customer?
--     - dim_account: what account was involved?
--     - dim_date: when did it happen?
--     - dim_district: where is the customer located?
--
--   FACT table (fct_): records measurable EVENTS
--     - fct_transactions: each row = one banking transaction with amounts
--
--   Notice we now use proper data types (INT, DATE, DECIMAL) instead of VARCHAR.
--   This is because we clean and cast the data during transformation.
--
--   SURROGATE KEYS: We use the original IDs as primary keys here for simplicity.
--   In enterprise settings, you'd often generate new integer surrogate keys.

USE DATABASE FINFLOW;
USE SCHEMA ANALYTICS;

-- Dimension: Date (one row per calendar date)
CREATE OR REPLACE TABLE DIM_DATE (
    DATE_KEY        DATE        NOT NULL PRIMARY KEY,
    YEAR            INT         NOT NULL,
    MONTH           INT         NOT NULL,
    DAY             INT         NOT NULL,
    DAY_OF_WEEK     INT,
    MONTH_NAME      VARCHAR(20),
    QUARTER         INT
);

-- Dimension: Customer
CREATE OR REPLACE TABLE DIM_CUSTOMER (
    CUSTOMER_KEY    INT         NOT NULL PRIMARY KEY,
    BIRTH_DATE      DATE,
    GENDER          VARCHAR(10),
    DISTRICT_ID     INT
);

-- Dimension: Account
CREATE OR REPLACE TABLE DIM_ACCOUNT (
    ACCOUNT_KEY     INT         NOT NULL PRIMARY KEY,
    DISTRICT_ID     INT,
    FREQUENCY       VARCHAR(50),
    OPEN_DATE       DATE
);

-- Dimension: District (location/geography)
CREATE OR REPLACE TABLE DIM_DISTRICT (
    DISTRICT_KEY    INT         NOT NULL PRIMARY KEY,
    DISTRICT_NAME   VARCHAR(100),
    REGION          VARCHAR(100),
    POPULATION      INT,
    AVG_SALARY      DECIMAL(12,2)
);

-- Fact: Transactions (the core event table — GRAIN: one row per transaction)
CREATE OR REPLACE TABLE FCT_TRANSACTIONS (
    TRANSACTION_KEY INT         NOT NULL PRIMARY KEY,
    ACCOUNT_KEY     INT         NOT NULL,
    TRANSACTION_DATE DATE       NOT NULL,
    TYPE            VARCHAR(20),
    OPERATION       VARCHAR(50),
    AMOUNT          DECIMAL(12,2),
    BALANCE         DECIMAL(12,2),
    K_SYMBOL        VARCHAR(50)
)

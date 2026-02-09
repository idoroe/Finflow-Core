-- 02_create_analytics_tables.sql
-- Creates the star schema tables in the ANALYTICS schema.
--
-- HIGH-LEVEL EXPLANATION:
--   This is the STAR SCHEMA — the clean, analytics-ready layer.
--
--   DIMENSION tables (dim_): describe WHO, WHAT, WHERE, WHEN
--   FACT table (fct_): records measurable EVENTS
--
--   Notice we now use proper data types (INT, DATE, DECIMAL) instead of VARCHAR.
--   The district columns A1-A16 are now given meaningful names.
--   Gender is decoded from the birth_number field.

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

-- Dimension: Customer (decoded from client + birth_number)
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

-- Dimension: District (A1-A16 columns renamed to meaningful names)
CREATE OR REPLACE TABLE DIM_DISTRICT (
    DISTRICT_KEY    INT         NOT NULL PRIMARY KEY,
    DISTRICT_NAME   VARCHAR(100),
    REGION          VARCHAR(100),
    POPULATION      INT,
    NUM_MUNICIPALITIES_LT_499   INT,
    NUM_MUNICIPALITIES_500_1999 INT,
    NUM_MUNICIPALITIES_2000_9999 INT,
    NUM_CITIES                  INT,
    URBAN_RATIO     DECIMAL(5,1),
    AVG_SALARY      INT,
    UNEMPLOYMENT_95 DECIMAL(5,2),
    UNEMPLOYMENT_96 DECIMAL(5,2),
    NUM_ENTREPRENEURS INT,
    NUM_CRIMES_95   INT,
    NUM_CRIMES_96   INT
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

-- 01_create_raw_tables.sql
-- Creates staging (RAW) tables that match the actual Czech banking CSV files.
--
-- HIGH-LEVEL EXPLANATION:
--   These tables are the first landing zone for data. They mirror the CSV columns
--   exactly. We use VARCHAR for most columns because raw data is messy — we'll
--   cast to proper types (INT, DATE, DECIMAL) during the transform step.
--
--   We have 8 CSV files, so we create 8 RAW tables.
--   "CREATE OR REPLACE" makes this idempotent — safe to run multiple times.

USE DATABASE FINFLOW;
USE SCHEMA RAW;

-- account.csv: one row per bank account
CREATE OR REPLACE TABLE ACCOUNT (
    ACCOUNT_ID      VARCHAR,
    DISTRICT_ID     VARCHAR,
    FREQUENCY       VARCHAR,
    DATE            VARCHAR
);

-- card.csv: one row per bank card issued
CREATE OR REPLACE TABLE CARD (
    CARD_ID         VARCHAR,
    DISP_ID         VARCHAR,
    TYPE            VARCHAR,
    ISSUED          VARCHAR
);

-- client.csv: one row per customer
-- NOTE: birth_number encodes BOTH birthday and gender
--   Format: YYMMDD — for women, month is increased by 50
--   e.g., 706213 = born 1970-12-13, female (62 = 12 + 50)
--   e.g., 450204 = born 1945-02-04, male
CREATE OR REPLACE TABLE CLIENT (
    CLIENT_ID       VARCHAR,
    BIRTH_NUMBER    VARCHAR,
    DISTRICT_ID     VARCHAR
);

-- disp.csv: disposition — links clients to accounts
-- A client can be an OWNER or DISPONENT (authorized user) of an account
CREATE OR REPLACE TABLE DISP (
    DISP_ID         VARCHAR,
    CLIENT_ID       VARCHAR,
    ACCOUNT_ID      VARCHAR,
    TYPE            VARCHAR
);

-- district.csv: geographic/demographic data
-- Original columns are named A1-A16, we keep them as-is in RAW
-- and rename them during transformation to ANALYTICS
CREATE OR REPLACE TABLE DISTRICT (
    A1              VARCHAR,
    A2              VARCHAR,
    A3              VARCHAR,
    A4              VARCHAR,
    A5              VARCHAR,
    A6              VARCHAR,
    A7              VARCHAR,
    A8              VARCHAR,
    A9              VARCHAR,
    A10             VARCHAR,
    A11             VARCHAR,
    A12             VARCHAR,
    A13             VARCHAR,
    A14             VARCHAR,
    A15             VARCHAR,
    A16             VARCHAR
);

-- loan.csv: one row per loan issued
CREATE OR REPLACE TABLE LOAN (
    LOAN_ID         VARCHAR,
    ACCOUNT_ID      VARCHAR,
    DATE            VARCHAR,
    AMOUNT          VARCHAR,
    DURATION        VARCHAR,
    PAYMENTS        VARCHAR,
    STATUS          VARCHAR
);

-- order.csv: standing orders (recurring automatic payments)
CREATE OR REPLACE TABLE "ORDER" (
    ORDER_ID        VARCHAR,
    ACCOUNT_ID      VARCHAR,
    BANK_TO         VARCHAR,
    ACCOUNT_TO      VARCHAR,
    AMOUNT          VARCHAR,
    K_SYMBOL        VARCHAR
);

-- trans.csv: one row per banking transaction (the main event table — ~1M rows)
CREATE OR REPLACE TABLE TRANS (
    TRANS_ID        VARCHAR,
    ACCOUNT_ID      VARCHAR,
    DATE            VARCHAR,
    TYPE            VARCHAR,
    OPERATION       VARCHAR,
    AMOUNT          VARCHAR,
    BALANCE         VARCHAR,
    K_SYMBOL        VARCHAR,
    BANK            VARCHAR,
    ACCOUNT         VARCHAR
)

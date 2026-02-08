-- 01_create_raw_tables.sql
-- Creates staging (RAW) tables that match the CSV file structure.
--
-- HIGH-LEVEL EXPLANATION:
--   These tables are the first landing zone for data. They mirror the CSV columns
--   exactly. We use VARCHAR for most columns because raw data is messy — we'll
--   cast to proper types (INT, DATE, DECIMAL) during the transform step.
--
--   "CREATE OR REPLACE" makes this idempotent — safe to run multiple times.
--   Each run drops and recreates the table structure.
--
-- NOTE: You will customize these tables once you choose your dataset.
--       The tables below are a template for a typical banking dataset.

USE DATABASE FINFLOW;
USE SCHEMA RAW;

-- Accounts: one row per bank account
CREATE OR REPLACE TABLE ACCOUNTS (
    ACCOUNT_ID      VARCHAR,
    DISTRICT_ID     VARCHAR,
    FREQUENCY       VARCHAR,
    DATE            VARCHAR,
    ACCOUNT_TYPE    VARCHAR
);

-- Clients: one row per customer
CREATE OR REPLACE TABLE CLIENTS (
    CLIENT_ID       VARCHAR,
    BIRTH_DATE      VARCHAR,
    GENDER          VARCHAR,
    DISTRICT_ID     VARCHAR
);

-- Transactions: one row per banking transaction (this is the main event table)
CREATE OR REPLACE TABLE TRANSACTIONS (
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
);

-- Districts: geographic/demographic info
CREATE OR REPLACE TABLE DISTRICTS (
    DISTRICT_ID     VARCHAR,
    DISTRICT_NAME   VARCHAR,
    REGION          VARCHAR,
    POPULATION      VARCHAR,
    AVG_SALARY      VARCHAR
);

-- Loans: one row per loan issued
CREATE OR REPLACE TABLE LOANS (
    LOAN_ID         VARCHAR,
    ACCOUNT_ID      VARCHAR,
    DATE            VARCHAR,
    AMOUNT          VARCHAR,
    DURATION        VARCHAR,
    PAYMENTS        VARCHAR,
    STATUS          VARCHAR
)

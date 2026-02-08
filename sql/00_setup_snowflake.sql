-- 00_setup_snowflake.sql
-- Creates the Snowflake database, schemas, and warehouse for FinFlow Core.
--
-- HIGH-LEVEL EXPLANATION:
--   Before we can store any data, we need to create the "containers" in Snowflake:
--     - DATABASE: like a folder that holds all your tables
--     - SCHEMA: a sub-folder within the database (we use RAW and ANALYTICS)
--     - WAREHOUSE: the compute engine that runs your queries (you pay for this)
--
--   "CREATE OR REPLACE" means: if it already exists, recreate it.
--   "IF NOT EXISTS" means: only create if it doesn't exist yet (safer).
--
-- RUN THIS: Copy-paste into Snowflake's web UI (Snowsight) the FIRST time,
--           or let run_all.py execute it automatically.

-- Create the database
CREATE DATABASE IF NOT EXISTS FINFLOW;

-- Create two schemas: RAW for staging data, ANALYTICS for the star schema
CREATE SCHEMA IF NOT EXISTS FINFLOW.RAW;
CREATE SCHEMA IF NOT EXISTS FINFLOW.ANALYTICS;

-- Create a small warehouse (XS = extra small = cheapest)
-- AUTO_SUSPEND = 60 means it shuts off after 60 seconds of no use (saves money)
-- AUTO_RESUME = TRUE means it turns back on automatically when you run a query
CREATE WAREHOUSE IF NOT EXISTS FINFLOW_XS
  WITH WAREHOUSE_SIZE = 'XSMALL'
  AUTO_SUSPEND = 60
  AUTO_RESUME = TRUE
  INITIALLY_SUSPENDED = TRUE

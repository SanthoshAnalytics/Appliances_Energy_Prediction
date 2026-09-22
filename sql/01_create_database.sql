-- ==================================================
-- 01_create_database.sql
-- Energy Consumption Forecasting & Analytics
-- ==================================================

-- Create database if it does not already exist
CREATE DATABASE IF NOT EXISTS energy_consumption_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

-- Set current database context
USE energy_consumption_db;

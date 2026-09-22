-- ==================================================
-- 03_load_data.sql
-- Bulk Data Loading Script for MySQL Workbench
-- ==================================================

USE energy_consumption_db;

-- Option 1: Using LOAD DATA LOCAL INFILE
-- Ensure local_infile=1 is enabled on both client and MySQL server.
/*
LOAD DATA LOCAL INFILE 'Data/energydata_complete.csv'
INTO TABLE energy_consumption
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(date, Appliances, lights, T1, RH_1, T2, RH_2, T3, RH_3, T4, RH_4, T5, RH_5, T6, RH_6, T7, RH_7, T8, RH_8, T9, RH_9, T_out, Press_mm_hg, RH_out, Windspeed, Visibility, Tdewpoint, rv1, rv2);
*/

-- Option 2: Python Automatic Database Loader
-- Run: python sql/load_data_mysql.py
-- This imports all 19,735 rows reliably via PyMySQL / SQLAlchemy.

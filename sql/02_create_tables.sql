-- ==================================================
-- 02_create_tables.sql
-- Energy Consumption Table Schema Definition
-- ==================================================

USE energy_consumption_db;

-- Drop table if it exists to allow clean re-runs
DROP TABLE IF EXISTS energy_consumption;

-- Create main table for energy consumption dataset
CREATE TABLE energy_consumption (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATETIME NOT NULL,
    Appliances INT NOT NULL,
    lights INT NOT NULL,
    T1 DECIMAL(6,2),
    RH_1 DECIMAL(6,2),
    T2 DECIMAL(6,2),
    RH_2 DECIMAL(6,2),
    T3 DECIMAL(6,2),
    RH_3 DECIMAL(6,2),
    T4 DECIMAL(6,2),
    RH_4 DECIMAL(6,2),
    T5 DECIMAL(6,2),
    RH_5 DECIMAL(6,2),
    T6 DECIMAL(6,2),
    RH_6 DECIMAL(6,2),
    T7 DECIMAL(6,2),
    RH_7 DECIMAL(6,2),
    T8 DECIMAL(6,2),
    RH_8 DECIMAL(6,2),
    T9 DECIMAL(6,2),
    RH_9 DECIMAL(6,2),
    T_out DECIMAL(6,2),
    Press_mm_hg DECIMAL(7,2),
    RH_out DECIMAL(6,2),
    Windspeed DECIMAL(6,2),
    Visibility DECIMAL(6,2),
    Tdewpoint DECIMAL(6,2),
    rv1 DECIMAL(10,6),
    rv2 DECIMAL(10,6),
    INDEX idx_date (date)
);

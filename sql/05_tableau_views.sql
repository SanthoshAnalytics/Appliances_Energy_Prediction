-- ==================================================
-- 05_tableau_views.sql
-- Tableau-Ready Aggregated Database Views
-- ==================================================

USE energy_consumption_db;

-- --------------------------------------------------
-- 1. Daily Energy View
-- --------------------------------------------------
CREATE OR REPLACE VIEW vw_daily_energy AS
SELECT 
    DATE(date) AS date,
    DAYNAME(date) AS day_name,
    DAYOFWEEK(date) AS day_of_week,
    CASE WHEN DAYOFWEEK(date) IN (1, 7) THEN 1 ELSE 0 END AS is_weekend,
    SUM(Appliances) AS total_appliances_wh,
    ROUND(AVG(Appliances), 2) AS avg_appliances_wh,
    SUM(lights) AS total_lights_wh,
    ROUND(AVG(T_out), 2) AS avg_outdoor_temp_c,
    ROUND(AVG(RH_out), 2) AS avg_outdoor_humidity_pct,
    ROUND(AVG(Windspeed), 2) AS avg_windspeed_mps
FROM energy_consumption
GROUP BY DATE(date), DAYNAME(date), DAYOFWEEK(date);

-- --------------------------------------------------
-- 2. Monthly Energy View
-- --------------------------------------------------
CREATE OR REPLACE VIEW vw_monthly_energy AS
SELECT 
    YEAR(date) AS year,
    MONTH(date) AS month,
    MONTHNAME(date) AS month_name,
    DATE_FORMAT(date, '%Y-%m') AS year_month,
    SUM(Appliances) AS total_appliances_wh,
    ROUND(AVG(Appliances), 2) AS avg_appliances_wh,
    MAX(Appliances) AS peak_appliances_wh,
    MIN(Appliances) AS min_appliances_wh,
    ROUND(AVG(T_out), 2) AS avg_outdoor_temp_c,
    ROUND(AVG(RH_out), 2) AS avg_outdoor_humidity_pct
FROM energy_consumption
GROUP BY YEAR(date), MONTH(date), MONTHNAME(date), DATE_FORMAT(date, '%Y-%m');

-- --------------------------------------------------
-- 3. Hourly Energy View
-- --------------------------------------------------
CREATE OR REPLACE VIEW vw_hourly_energy AS
SELECT 
    HOUR(date) AS hour_of_day,
    ROUND(AVG(Appliances), 2) AS avg_appliances_wh,
    SUM(Appliances) AS total_appliances_wh,
    ROUND(AVG(lights), 2) AS avg_lights_wh,
    ROUND(AVG(T1), 2) AS avg_indoor_temp_c,
    ROUND(AVG(RH_1), 2) AS avg_indoor_humidity_pct
FROM energy_consumption
GROUP BY HOUR(date);

-- --------------------------------------------------
-- 4. Weekday vs Weekend View
-- --------------------------------------------------
CREATE OR REPLACE VIEW vw_weekday_energy AS
SELECT 
    HOUR(date) AS hour_of_day,
    CASE WHEN DAYOFWEEK(date) IN (1, 7) THEN 'Weekend' ELSE 'Weekday' END AS day_type,
    ROUND(AVG(Appliances), 2) AS avg_appliances_wh,
    ROUND(AVG(T_out), 2) AS avg_outdoor_temp_c,
    ROUND(AVG(Windspeed), 2) AS avg_windspeed_mps
FROM energy_consumption
GROUP BY HOUR(date), day_type;

-- --------------------------------------------------
-- 5. Environmental Energy View
-- --------------------------------------------------
CREATE OR REPLACE VIEW vw_environmental_energy AS
SELECT 
    date,
    Appliances,
    lights,
    T1 AS temp_kitchen_c,
    RH_1 AS humidity_kitchen_pct,
    T2 AS temp_living_c,
    RH_2 AS humidity_living_pct,
    T6 AS temp_outside_building_c,
    RH_6 AS humidity_outside_building_pct,
    T_out AS temp_outdoor_weather_c,
    RH_out AS humidity_outdoor_weather_pct,
    Windspeed AS windspeed_mps,
    Visibility AS visibility_km,
    Tdewpoint AS dewpoint_c
FROM energy_consumption;

-- --------------------------------------------------
-- 6. Forecast Comparison View Schema
-- --------------------------------------------------
CREATE OR REPLACE VIEW vw_forecast AS
SELECT 
    date,
    Appliances AS actual_appliances,
    CAST(NULL AS DECIMAL(10,2)) AS predicted_appliances,
    'Historical' AS record_type
FROM energy_consumption;

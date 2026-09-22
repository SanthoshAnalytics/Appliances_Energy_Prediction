-- ==================================================
-- 04_analysis_queries.sql
-- 20 Analytical SQL Queries for Energy Consumption DB
-- ==================================================

USE energy_consumption_db;

-- --------------------------------------------------
-- 1. Total Energy Consumption
-- --------------------------------------------------
SELECT SUM(Appliances) AS total_energy_wh
FROM energy_consumption;

-- --------------------------------------------------
-- 2. Average Energy Consumption
-- --------------------------------------------------
SELECT ROUND(AVG(Appliances), 2) AS avg_energy_wh
FROM energy_consumption;

-- --------------------------------------------------
-- 3. Maximum Energy Consumption
-- --------------------------------------------------
SELECT MAX(Appliances) AS max_energy_wh
FROM energy_consumption;

-- --------------------------------------------------
-- 4. Minimum Energy Consumption
-- --------------------------------------------------
SELECT MIN(Appliances) AS min_energy_wh
FROM energy_consumption;

-- --------------------------------------------------
-- 5. Daily Average Consumption
-- --------------------------------------------------
SELECT 
    DATE(date) AS consumption_date,
    ROUND(AVG(Appliances), 2) AS daily_avg_wh
FROM energy_consumption
GROUP BY DATE(date)
ORDER BY consumption_date;

-- --------------------------------------------------
-- 6. Daily Total Consumption
-- --------------------------------------------------
SELECT 
    DATE(date) AS consumption_date,
    SUM(Appliances) AS daily_total_wh
FROM energy_consumption
GROUP BY DATE(date)
ORDER BY consumption_date;

-- --------------------------------------------------
-- 7. Monthly Total & Average Consumption
-- --------------------------------------------------
SELECT 
    DATE_FORMAT(date, '%Y-%m') AS year_month,
    SUM(Appliances) AS monthly_total_wh,
    ROUND(AVG(Appliances), 2) AS monthly_avg_wh
FROM energy_consumption
GROUP BY DATE_FORMAT(date, '%Y-%m')
ORDER BY year_month;

-- --------------------------------------------------
-- 8. Hourly Average Consumption
-- --------------------------------------------------
SELECT 
    HOUR(date) AS hour_of_day,
    ROUND(AVG(Appliances), 2) AS hourly_avg_wh
FROM energy_consumption
GROUP BY HOUR(date)
ORDER BY hour_of_day;

-- --------------------------------------------------
-- 9. Peak Consumption Hour
-- --------------------------------------------------
SELECT 
    HOUR(date) AS peak_hour,
    ROUND(AVG(Appliances), 2) AS avg_energy_wh
FROM energy_consumption
GROUP BY HOUR(date)
ORDER BY avg_energy_wh DESC
LIMIT 1;

-- --------------------------------------------------
-- 10. Weekend vs Weekday Average Consumption
-- --------------------------------------------------
SELECT 
    CASE 
        WHEN DAYOFWEEK(date) IN (1, 7) THEN 'Weekend'
        ELSE 'Weekday'
    END AS day_type,
    ROUND(AVG(Appliances), 2) AS avg_energy_wh,
    SUM(Appliances) AS total_energy_wh
FROM energy_consumption
GROUP BY day_type;

-- --------------------------------------------------
-- 11. Average Indoor vs Outdoor Temperature
-- --------------------------------------------------
SELECT 
    ROUND(AVG(T1), 2) AS avg_living_room_temp_c,
    ROUND(AVG(T2), 2) AS avg_kitchen_temp_c,
    ROUND(AVG(T_out), 2) AS avg_outdoor_temp_c
FROM energy_consumption;

-- --------------------------------------------------
-- 12. Temperature vs Energy Consumption Relationship
-- --------------------------------------------------
SELECT 
    FLOOR(T_out) AS outdoor_temp_bin_c,
    ROUND(AVG(Appliances), 2) AS avg_energy_wh,
    COUNT(*) AS sample_count
FROM energy_consumption
GROUP BY FLOOR(T_out)
ORDER BY outdoor_temp_bin_c;

-- --------------------------------------------------
-- 13. Indoor Humidity vs Energy Consumption
-- --------------------------------------------------
SELECT 
    FLOOR(RH_1 / 5) * 5 AS rh1_bin_pct,
    ROUND(AVG(Appliances), 2) AS avg_energy_wh
FROM energy_consumption
GROUP BY rh1_bin_pct
ORDER BY rh1_bin_pct;

-- --------------------------------------------------
-- 14. Wind Speed vs Energy Consumption
-- --------------------------------------------------
SELECT 
    FLOOR(Windspeed) AS windspeed_bin_mps,
    ROUND(AVG(Appliances), 2) AS avg_energy_wh
FROM energy_consumption
GROUP BY FLOOR(Windspeed)
ORDER BY windspeed_bin_mps;

-- --------------------------------------------------
-- 15. Top 10 Consumption Periods (10-min intervals)
-- --------------------------------------------------
SELECT 
    date,
    Appliances,
    T_out,
    RH_out,
    Windspeed
FROM energy_consumption
ORDER BY Appliances DESC
LIMIT 10;

-- --------------------------------------------------
-- 16. Highest Energy Consumption Days
-- --------------------------------------------------
SELECT 
    DATE(date) AS consumption_date,
    SUM(Appliances) AS total_daily_wh
FROM energy_consumption
GROUP BY DATE(date)
ORDER BY total_daily_wh DESC
LIMIT 5;

-- --------------------------------------------------
-- 17. Lowest Energy Consumption Days
-- --------------------------------------------------
SELECT 
    DATE(date) AS consumption_date,
    SUM(Appliances) AS total_daily_wh
FROM energy_consumption
GROUP BY DATE(date)
ORDER BY total_daily_wh ASC
LIMIT 5;

-- --------------------------------------------------
-- 18. Monthly Consumption Trend Analysis
-- --------------------------------------------------
SELECT 
    DATE_FORMAT(date, '%Y-%m') AS year_month,
    MIN(Appliances) AS min_wh,
    MAX(Appliances) AS max_wh,
    ROUND(AVG(Appliances), 2) AS avg_wh,
    SUM(Appliances) AS total_wh
FROM energy_consumption
GROUP BY DATE_FORMAT(date, '%Y-%m')
ORDER BY year_month;

-- --------------------------------------------------
-- 19. Hourly Consumption Trend Across Weekdays vs Weekends
-- --------------------------------------------------
SELECT 
    HOUR(date) AS hour_of_day,
    CASE 
        WHEN DAYOFWEEK(date) IN (1, 7) THEN 'Weekend'
        ELSE 'Weekday'
    END AS day_type,
    ROUND(AVG(Appliances), 2) AS avg_energy_wh
FROM energy_consumption
GROUP BY hour_of_day, day_type
ORDER BY hour_of_day, day_type;

-- --------------------------------------------------
-- 20. Rolling 6-Period Moving Average (1 Hour Window)
-- --------------------------------------------------
SELECT 
    date,
    Appliances,
    ROUND(AVG(Appliances) OVER (
        ORDER BY date 
        ROWS BETWEEN 5 PRECEDING AND CURRENT ROW
    ), 2) AS rolling_avg_1h_wh
FROM energy_consumption
LIMIT 100;

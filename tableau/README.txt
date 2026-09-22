==================================================
TABLEAU DATASETS & DASHBOARD GUIDE
==================================================

Project: ENERGY CONSUMPTION FORECASTING AND ANALYTICS

The CSV files in this folder are prepared specifically for building
interactive dashboards in Tableau Desktop or Tableau Public.

--------------------------------------------------
DATASET MAPPING FOR TABLEAU DASHBOARD SHEETS:
--------------------------------------------------

1. daily_energy.csv
   - Purpose: KPI cards and Daily Energy Consumption Trend line charts.
   - Fields: date, day_name, is_weekend, total_appliances_wh, avg_appliances_wh,
             total_lights_wh, avg_outdoor_temp_c, avg_outdoor_humidity_pct, avg_windspeed_mps.
   - Use Cases: Daily energy trends, weekend vs weekday comparisons, KPI totals.

2. monthly_energy.csv
   - Purpose: Monthly consumption summaries and high-level volume metrics.
   - Fields: year_month, month_name, total_appliances_wh, avg_appliances_wh,
             peak_appliances_wh, min_appliances_wh, avg_outdoor_temp_c, avg_outdoor_humidity_pct.
   - Use Cases: Monthly total bar charts, seasonal volume trends.

3. hourly_energy.csv
   - Purpose: Hourly demand patterns and peak hour identification.
   - Fields: hour_of_day (0-23), avg_appliances_wh, total_appliances_wh, avg_lights_wh,
             avg_indoor_temp_c, avg_indoor_humidity_pct.
   - Use Cases: Hourly demand bar charts, peak load identification (17:00 - 20:00 PM peak).

4. environment_energy.csv
   - Purpose: Environmental & weather correlation analysis.
   - Fields: date, Appliances, lights, T1 (kitchen temp), RH_1 (kitchen humidity),
             T2 (living room temp), RH_2, T6 (outside building temp), RH_6, T_out (weather temp),
             RH_out, Windspeed, Visibility, Tdewpoint.
   - Use Cases: Temperature vs Energy scatter plots, humidity vs energy dual-axis charts.

5. forecast.csv
   - Purpose: Actual vs Predicted model evaluation and 24-Hour Future Forecast.
   - Fields: date, actual_Appliances, predicted_Appliances, record_type ('Test Evaluation', 'Future Forecast').
   - Use Cases: Dual-line chart comparing Actual vs Predicted, out-of-sample future forecast curve.

--------------------------------------------------
HOW TO CONNECT IN TABLEAU DESKTOP:
--------------------------------------------------
1. Open Tableau Desktop.
2. Under "Connect -> To a File", select "Text File".
3. Navigate to this tableau/ folder and select any of the CSV files.
4. Drag tables to build relationships or connect to individual files for dedicated sheets.
5. Create your dashboard and save as .twbx or publish to Tableau Public.

"""
Clean Tableau Dataset Exporter & Folder Sanitizer.
Removes invalid .twb XML, temporary files, and duplicate datasets.
Generates 5 clean, distinct Tableau-ready CSV files and a README.txt inside tableau/ folder.
"""

from pathlib import Path
import pandas as pd
import numpy as np


def prepare_tableau_files():
    project_root = Path(__file__).resolve().parent.parent
    tableau_dir = project_root / "tableau"
    data_dir = project_root / "Data"
    outputs_dir = project_root / "outputs"

    tableau_dir.mkdir(parents=True, exist_ok=True)

    print("Cleaning tableau/ directory...")
    # Remove invalid twb, html, master csv, or temporary files
    for item in tableau_dir.glob("*"):
        if item.is_file():
            item.unlink()
            print(f"Removed file: {item.name}")

    cleaned_path = data_dir / "energy_consumption_cleaned.csv"
    if not cleaned_path.exists():
        raise FileNotFoundError(f"Missing required dataset: {cleaned_path}")

    df = pd.read_csv(cleaned_path)
    df["date"] = pd.to_datetime(df["date"])

    # 1. daily_energy.csv (For Daily Trends & KPI cards)
    df["date_only"] = df["date"].dt.date
    daily_df = df.groupby("date_only").agg(
        total_appliances_wh=("Appliances", "sum"),
        avg_appliances_wh=("Appliances", "mean"),
        total_lights_wh=("lights", "sum"),
        avg_outdoor_temp_c=("T_out", "mean"),
        avg_outdoor_humidity_pct=("RH_out", "mean"),
        avg_windspeed_mps=("Windspeed", "mean")
    ).reset_index()

    daily_df["date"] = pd.to_datetime(daily_df["date_only"])
    daily_df["day_name"] = daily_df["date"].dt.day_name()
    daily_df["is_weekend"] = (daily_df["date"].dt.dayofweek >= 5).astype(int)
    
    daily_df = daily_df[["date", "day_name", "is_weekend", "total_appliances_wh", "avg_appliances_wh", "total_lights_wh", "avg_outdoor_temp_c", "avg_outdoor_humidity_pct", "avg_windspeed_mps"]]
    daily_df["avg_appliances_wh"] = daily_df["avg_appliances_wh"].round(2)
    daily_df["avg_outdoor_temp_c"] = daily_df["avg_outdoor_temp_c"].round(2)
    daily_df["avg_outdoor_humidity_pct"] = daily_df["avg_outdoor_humidity_pct"].round(2)
    daily_df["avg_windspeed_mps"] = daily_df["avg_windspeed_mps"].round(2)

    daily_path = tableau_dir / "daily_energy.csv"
    daily_df.to_csv(daily_path, index=False)
    print(f"Created: {daily_path} ({len(daily_df)} rows)")

    # 2. monthly_energy.csv (For Monthly Overview)
    df["year_month"] = df["date"].dt.to_period("M").astype(str)
    monthly_df = df.groupby("year_month").agg(
        total_appliances_wh=("Appliances", "sum"),
        avg_appliances_wh=("Appliances", "mean"),
        peak_appliances_wh=("Appliances", "max"),
        min_appliances_wh=("Appliances", "min"),
        avg_outdoor_temp_c=("T_out", "mean"),
        avg_outdoor_humidity_pct=("RH_out", "mean")
    ).reset_index()

    monthly_df["month_name"] = pd.to_datetime(monthly_df["year_month"] + "-01").dt.month_name()
    monthly_df = monthly_df[["year_month", "month_name", "total_appliances_wh", "avg_appliances_wh", "peak_appliances_wh", "min_appliances_wh", "avg_outdoor_temp_c", "avg_outdoor_humidity_pct"]]
    monthly_df["avg_appliances_wh"] = monthly_df["avg_appliances_wh"].round(2)
    monthly_df["avg_outdoor_temp_c"] = monthly_df["avg_outdoor_temp_c"].round(2)
    monthly_df["avg_outdoor_humidity_pct"] = monthly_df["avg_outdoor_humidity_pct"].round(2)

    monthly_path = tableau_dir / "monthly_energy.csv"
    monthly_df.to_csv(monthly_path, index=False)
    print(f"Created: {monthly_path} ({len(monthly_df)} rows)")

    # 3. hourly_energy.csv (For Hourly Demand Patterns & Peak Hour Analysis)
    df["hour"] = df["date"].dt.hour
    hourly_df = df.groupby("hour").agg(
        avg_appliances_wh=("Appliances", "mean"),
        total_appliances_wh=("Appliances", "sum"),
        avg_lights_wh=("lights", "mean"),
        avg_indoor_temp_c=("T1", "mean"),
        avg_indoor_humidity_pct=("RH_1", "mean")
    ).reset_index()

    hourly_df.rename(columns={"hour": "hour_of_day"}, inplace=True)
    hourly_df["avg_appliances_wh"] = hourly_df["avg_appliances_wh"].round(2)
    hourly_df["avg_lights_wh"] = hourly_df["avg_lights_wh"].round(2)
    hourly_df["avg_indoor_temp_c"] = hourly_df["avg_indoor_temp_c"].round(2)
    hourly_df["avg_indoor_humidity_pct"] = hourly_df["avg_indoor_humidity_pct"].round(2)

    hourly_path = tableau_dir / "hourly_energy.csv"
    hourly_df.to_csv(hourly_path, index=False)
    print(f"Created: {hourly_path} ({len(hourly_df)} rows)")

    # 4. environment_energy.csv (For Temperature & Humidity Correlations)
    env_cols = ["date", "Appliances", "lights", "T1", "RH_1", "T2", "RH_2", "T6", "RH_6", "T_out", "RH_out", "Windspeed", "Visibility", "Tdewpoint"]
    env_df = df[env_cols].copy()
    env_path = tableau_dir / "environment_energy.csv"
    env_df.to_csv(env_path, index=False)
    print(f"Created: {env_path} ({len(env_df)} rows)")

    # 5. forecast.csv (For Actual vs Predicted Evaluation & 24h Future Forecast)
    test_preds_path = outputs_dir / "test_predictions.csv"
    future_forecast_path = outputs_dir / "future_energy_forecast.csv"

    forecast_rows = []
    if test_preds_path.exists():
        test_preds = pd.read_csv(test_preds_path)
        lr_preds = test_preds[test_preds["model"] == "Linear Regression"]
        for _, row in lr_preds.iterrows():
            forecast_rows.append({
                "date": row["date"],
                "actual_Appliances": float(row["actual"]),
                "predicted_Appliances": round(float(row["predicted"]), 2),
                "record_type": "Test Evaluation"
            })

    if future_forecast_path.exists():
        future_fc = pd.read_csv(future_forecast_path)
        for _, row in future_fc.iterrows():
            forecast_rows.append({
                "date": row["date"],
                "actual_Appliances": np.nan,
                "predicted_Appliances": round(float(row["predicted_Appliances"]), 2),
                "record_type": "Future Forecast"
            })

    forecast_df = pd.DataFrame(forecast_rows)
    forecast_path = tableau_dir / "forecast.csv"
    forecast_df.to_csv(forecast_path, index=False)
    print(f"Created: {forecast_path} ({len(forecast_df)} rows)")

    # 6. README.txt
    readme_content = """==================================================
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
"""

    readme_path = tableau_dir / "README.txt"
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(readme_content)
    print(f"Created: {readme_path}")


if __name__ == "__main__":
    prepare_tableau_files()

"""
Feature Engineering Module for Appliances Energy Prediction.
Creates calendar, lag, and rolling features strictly without data leakage.
Saves processed features to Data/energy_consumption_features.csv.
"""

from pathlib import Path
import pandas as pd
import numpy as np


def create_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Applies feature engineering pipeline to input DataFrame.
    """
    df = df.copy()

    # Ensure date column is datetime and sorted
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").reset_index(drop=True)

    # 1. Calendar Features
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    df["day"] = df["date"].dt.day
    df["hour"] = df["date"].dt.hour
    df["day_of_week"] = df["date"].dt.dayofweek
    df["is_weekend"] = (df["day_of_week"] >= 5).astype(int)

    # 2. Lag Features (Target: Appliances)
    # 10-minute frequency: 6 steps = 1 hour, 144 steps = 1 day, 1008 steps = 7 days
    df["lag_6"] = df["Appliances"].shift(6)
    df["lag_144"] = df["Appliances"].shift(144)
    df["lag_1008"] = df["Appliances"].shift(1008)

    # 3. Rolling Mean Features (Strict leakage prevention: shift(1) before rolling)
    df["rolling_mean_6"] = df["Appliances"].shift(1).rolling(6).mean()
    df["rolling_mean_144"] = df["Appliances"].shift(1).rolling(144).mean()

    # 4. Remove initial NaN rows created by lag/rolling shifts
    df_model = df.dropna().reset_index(drop=True)
    return df_model


def get_feature_columns() -> list:
    """
    Returns list of feature column names used for model training.
    """
    return [
        "lights",
        "T1",
        "RH_1",
        "T2",
        "RH_2",
        "T3",
        "RH_3",
        "T4",
        "RH_4",
        "T5",
        "RH_5",
        "T6",
        "RH_6",
        "T7",
        "RH_7",
        "T8",
        "RH_8",
        "T9",
        "RH_9",
        "T_out",
        "Press_mm_hg",
        "RH_out",
        "Windspeed",
        "Visibility",
        "Tdewpoint",
        "year",
        "month",
        "day",
        "hour",
        "day_of_week",
        "is_weekend",
        "lag_6",
        "lag_144",
        "lag_1008",
        "rolling_mean_6",
        "rolling_mean_144"
    ]


def run_feature_engineering() -> pd.DataFrame:
    """
    Executes feature engineering and saves dataset and feature list.
    """
    project_root = Path(__file__).resolve().parent.parent
    data_dir = project_root / "Data"
    outputs_dir = project_root / "outputs"
    outputs_dir.mkdir(parents=True, exist_ok=True)

    clean_path = data_dir / "energy_consumption_cleaned.csv"
    features_path = data_dir / "energy_consumption_features.csv"
    feature_list_path = outputs_dir / "feature_list.txt"

    print(f"Reading cleaned data from: {clean_path}")
    df_clean = pd.read_csv(clean_path)

    df_features = create_features(df_clean)
    df_features.to_csv(features_path, index=False)
    print(f"Feature dataset saved to: {features_path} (Shape: {df_features.shape})")

    features = get_feature_columns()
    with open(feature_list_path, "w") as f:
        for feat in features:
            f.write(f"{feat}\n")
    print(f"Feature list saved to: {feature_list_path} ({len(features)} features)")

    return df_features


if __name__ == "__main__":
    run_feature_engineering()

"""
Data Cleaning Module for Appliances Energy Prediction.
Handles data loading, date formatting, quality reporting, and saving cleaned data.
"""

from pathlib import Path
import pandas as pd
import numpy as np


def load_and_clean_data(raw_data_path: Path = None) -> pd.DataFrame:
    """
    Loads raw energy consumption data, parses date column, checks quality,
    and returns a cleaned DataFrame.
    """
    if raw_data_path is None:
        project_root = Path(__file__).resolve().parent.parent
        raw_data_path = project_root / "Data" / "energydata_complete.csv"

    print(f"Loading raw data from: {raw_data_path}")
    df = pd.read_csv(raw_data_path)

    # 1. Convert date column to datetime
    df["date"] = pd.to_datetime(df["date"])

    # 2. Sort chronologically
    df = df.sort_values("date").reset_index(drop=True)

    # 3. Check and drop duplicate dates if any
    duplicate_count = df.duplicated(subset=["date"]).sum()
    if duplicate_count > 0:
        print(f"Removing {duplicate_count} duplicate timestamps...")
        df = df.drop_duplicates(subset=["date"]).reset_index(drop=True)

    return df


def generate_quality_report(df: pd.DataFrame, output_dir: Path = None) -> pd.DataFrame:
    """
    Generates a data quality report CSV summarizing column types, nulls, min, max, mean, std.
    """
    if output_dir is None:
        output_dir = Path(__file__).resolve().parent.parent / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    report_rows = []
    for col in df.columns:
        col_type = str(df[col].dtype)
        null_count = int(df[col].isnull().sum())
        non_null_count = int(df[col].count())
        
        if pd.api.types.is_numeric_dtype(df[col]):
            min_val = float(df[col].min())
            max_val = float(df[col].max())
            mean_val = float(df[col].mean())
            std_val = float(df[col].std())
        else:
            min_val, max_val, mean_val, std_val = np.nan, np.nan, np.nan, np.nan

        report_rows.append({
            "column": col,
            "dtype": col_type,
            "null_count": null_count,
            "non_null_count": non_null_count,
            "min": min_val,
            "max": max_val,
            "mean": mean_val,
            "std": std_val
        })

    report_df = pd.DataFrame(report_rows)
    report_path = output_dir / "data_quality_report.csv"
    report_df.to_csv(report_path, index=False)
    print(f"Data quality report saved to: {report_path}")
    return report_df


def run_data_cleaning() -> pd.DataFrame:
    """
    Main function to execute data cleaning pipeline and save processed dataset.
    """
    project_root = Path(__file__).resolve().parent.parent
    data_dir = project_root / "Data"
    raw_path = data_dir / "energydata_complete.csv"
    clean_path = data_dir / "energy_consumption_cleaned.csv"

    df = load_and_clean_data(raw_path)
    generate_quality_report(df)

    df.to_csv(clean_path, index=False)
    print(f"Cleaned dataset saved to: {clean_path} (Shape: {df.shape})")
    return df


if __name__ == "__main__":
    run_data_cleaning()

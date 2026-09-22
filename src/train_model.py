"""
Model Training Module for Appliances Energy Prediction.
Trains 5 baseline and ML models using chronological 80/20 train/test split.
Evaluates models using MAE, MSE, RMSE, MAPE, and R2.
Saves model_comparison.csv and test_predictions.csv.
"""

from pathlib import Path
import pandas as pd
import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from xgboost import XGBRegressor

from feature_engineering import get_feature_columns


def calculate_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> dict:
    """
    Computes evaluation metrics: MAE, MSE, RMSE, MAPE, R2.
    """
    mae = mean_absolute_error(y_true, y_pred)
    mse = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    # Avoid division by zero in MAPE
    mape = np.mean(np.abs((y_true - y_pred) / np.maximum(np.abs(y_true), 1e-5))) * 100
    r2 = r2_score(y_true, y_pred)

    return {
        "MAE": round(mae, 4),
        "MSE": round(mse, 4),
        "RMSE": round(rmse, 4),
        "MAPE (%)": round(mape, 4),
        "R2": round(r2, 4)
    }


def train_and_evaluate_models(df: pd.DataFrame, train_ratio: float = 0.80) -> tuple:
    """
    Splits data chronologically and trains Baseline, Linear Regression,
    Random Forest, Gradient Boosting, and XGBoost models.
    Returns comparison DataFrame and test predictions DataFrame.
    """
    feature_cols = get_feature_columns()
    target_col = "Appliances"

    X = df[feature_cols]
    y = df[target_col]
    dates = df["date"]

    # Chronological 80/20 split (NO random shuffle)
    split_idx = int(len(df) * train_ratio)
    
    X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
    y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]
    dates_test = dates.iloc[split_idx:]

    print(f"Train period: {dates.iloc[0]} to {dates.iloc[split_idx - 1]} ({len(X_train)} samples)")
    print(f"Test period : {dates.iloc[split_idx]} to {dates.iloc[-1]} ({len(X_test)} samples)")

    models = {
        "Baseline (Prev Hour)": None,  # Handled separately with lag_6
        "Linear Regression": LinearRegression(),
        "Random Forest": RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1),
        "Gradient Boosting": GradientBoostingRegressor(n_estimators=100, random_state=42),
        "XGBoost": XGBRegressor(n_estimators=100, learning_rate=0.1, random_state=42, n_jobs=-1)
    }

    comparison_results = []
    test_preds_list = []

    for name, model in models.items():
        print(f"Evaluating {name}...")

        if name == "Baseline (Prev Hour)":
            # Naive baseline using lag_6 (previous hour value)
            y_pred = X_test["lag_6"].values
        else:
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)

        metrics = calculate_metrics(y_test.values, y_pred)
        metrics["Model"] = name
        comparison_results.append(metrics)

        # Store predictions
        pred_df = pd.DataFrame({
            "date": dates_test.values,
            "actual": y_test.values,
            "predicted": y_pred,
            "model": name
        })
        test_preds_list.append(pred_df)

    # Compile comparison table
    comp_df = pd.DataFrame(comparison_results)[["Model", "MAE", "MSE", "RMSE", "MAPE (%)", "R2"]]
    all_preds_df = pd.concat(test_preds_list, ignore_index=True)

    return comp_df, all_preds_df


def run_model_training() -> tuple:
    """
    Loads features dataset, trains baseline & ML models, saves evaluation outputs.
    """
    project_root = Path(__file__).resolve().parent.parent
    features_path = project_root / "Data" / "energy_consumption_features.csv"
    outputs_dir = project_root / "outputs"
    outputs_dir.mkdir(parents=True, exist_ok=True)

    print(f"Loading feature dataset from: {features_path}")
    df = pd.read_csv(features_path)

    comp_df, all_preds_df = train_and_evaluate_models(df)

    comp_path = outputs_dir / "model_comparison.csv"
    preds_path = outputs_dir / "test_predictions.csv"

    comp_df.to_csv(comp_path, index=False)
    all_preds_df.to_csv(preds_path, index=False)

    print(f"\nModel comparison saved to: {comp_path}")
    print(comp_df.to_string(index=False))
    print(f"\nTest predictions saved to: {preds_path}")

    return comp_df, all_preds_df


if __name__ == "__main__":
    run_model_training()

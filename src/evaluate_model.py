"""
Model Evaluation and Tuning Module for Appliances Energy Prediction.
Uses TimeSeriesSplit cross-validation to tune top ensemble models (RandomForest, GradientBoosting, XGBoost).
Saves final_model_comparison.csv, final_energy_forecasting_model.pkl, and feature_columns.pkl.
"""

from pathlib import Path
import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import TimeSeriesSplit, RandomizedSearchCV
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from xgboost import XGBRegressor

from feature_engineering import get_feature_columns
from train_model import calculate_metrics, train_and_evaluate_models


def tune_models(X_train: pd.DataFrame, y_train: pd.Series) -> dict:
    """
    Performs TimeSeriesSplit hyperparameter tuning for top ensemble models.
    Returns dictionary of tuned models.
    """
    print("Performing TimeSeriesSplit cross-validation tuning...")
    tscv = TimeSeriesSplit(n_splits=5)

    # 1. Random Forest Parameter Grid
    rf_param_grid = {
        "n_estimators": [100, 150],
        "max_depth": [10, 15, 20, None],
        "min_samples_split": [2, 5, 10],
        "max_features": ["sqrt", 1.0]
    }

    # 2. Gradient Boosting Parameter Grid
    gb_param_grid = {
        "n_estimators": [100, 150],
        "learning_rate": [0.03, 0.05, 0.1],
        "max_depth": [3, 5, 7],
        "subsample": [0.8, 1.0]
    }

    # 3. XGBoost Parameter Grid
    xgb_param_grid = {
        "n_estimators": [100, 150],
        "learning_rate": [0.03, 0.05, 0.1],
        "max_depth": [3, 5, 7],
        "subsample": [0.8, 1.0],
        "colsample_bytree": [0.8, 1.0]
    }

    # RandomizedSearchCV tuning for speed & student laptop friendly execution
    rf_search = RandomizedSearchCV(
        RandomForestRegressor(random_state=42, n_jobs=-1),
        param_distributions=rf_param_grid,
        n_iter=6,
        cv=tscv,
        scoring="neg_root_mean_squared_error",
        random_state=42,
        n_jobs=-1
    )
    rf_search.fit(X_train, y_train)
    best_rf = rf_search.best_estimator_
    print(f"Best RF Params: {rf_search.best_params_}")

    gb_search = RandomizedSearchCV(
        GradientBoostingRegressor(random_state=42),
        param_distributions=gb_param_grid,
        n_iter=6,
        cv=tscv,
        scoring="neg_root_mean_squared_error",
        random_state=42,
        n_jobs=-1
    )
    gb_search.fit(X_train, y_train)
    best_gb = gb_search.best_estimator_
    print(f"Best GB Params: {gb_search.best_params_}")

    xgb_search = RandomizedSearchCV(
        XGBRegressor(random_state=42, n_jobs=-1),
        param_distributions=xgb_param_grid,
        n_iter=6,
        cv=tscv,
        scoring="neg_root_mean_squared_error",
        random_state=42,
        n_jobs=-1
    )
    xgb_search.fit(X_train, y_train)
    best_xgb = xgb_search.best_estimator_
    print(f"Best XGB Params: {xgb_search.best_params_}")

    return {
        "Random Forest (Tuned)": best_rf,
        "Gradient Boosting (Tuned)": best_gb,
        "XGBoost (Tuned)": best_xgb
    }


def evaluate_and_select_best_model(df: pd.DataFrame, train_ratio: float = 0.80) -> tuple:
    """
    Evaluates baseline, untuned, and tuned models, selects the best model based on test RMSE,
    and returns final comparison table and best model object.
    """
    feature_cols = get_feature_columns()
    target_col = "Appliances"

    X = df[feature_cols]
    y = df[target_col]

    split_idx = int(len(df) * train_ratio)
    X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
    y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]

    # Get untuned model results
    untuned_comp, _ = train_and_evaluate_models(df, train_ratio)

    # Tune top models
    tuned_models = tune_models(X_train, y_train)

    tuned_results = []
    trained_objects = {}

    for name, model in tuned_models.items():
        print(f"Testing {name} on test set...")
        y_pred = model.predict(X_test)
        metrics = calculate_metrics(y_test.values, y_pred)
        metrics["Model"] = name
        tuned_results.append(metrics)
        trained_objects[name] = model

    tuned_comp = pd.DataFrame(tuned_results)[["Model", "MAE", "MSE", "RMSE", "MAPE (%)", "R2"]]

    # Combine untuned and tuned results
    final_comp = pd.concat([untuned_comp, tuned_comp], ignore_index=True)

    # Sort by RMSE (ascending)
    final_comp = final_comp.sort_values("RMSE").reset_index(drop=True)

    # Select best model
    best_model_name = final_comp.iloc[0]["Model"]
    best_rmse = final_comp.iloc[0]["RMSE"]
    print(f"\nBest Performing Model: '{best_model_name}' (Test RMSE: {best_rmse})")

    # Retrieve best model estimator
    if "Tuned" in best_model_name:
        best_model_obj = trained_objects[best_model_name]
    else:
        # Re-fit the best untuned model
        if "XGBoost" in best_model_name:
            best_model_obj = XGBRegressor(n_estimators=100, learning_rate=0.1, random_state=42, n_jobs=-1)
        elif "Random Forest" in best_model_name:
            best_model_obj = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
        elif "Gradient Boosting" in best_model_name:
            best_model_obj = GradientBoostingRegressor(n_estimators=100, random_state=42)
        else:
            best_model_obj = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
        best_model_obj.fit(X_train, y_train)

    return final_comp, best_model_obj, best_model_name


def run_model_evaluation() -> tuple:
    """
    Executes model evaluation, tuning, and artifact saving.
    """
    project_root = Path(__file__).resolve().parent.parent
    features_path = project_root / "Data" / "energy_consumption_features.csv"
    outputs_dir = project_root / "outputs"
    models_dir = project_root / "models"

    outputs_dir.mkdir(parents=True, exist_ok=True)
    models_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(features_path)

    final_comp, best_model_obj, best_model_name = evaluate_and_select_best_model(df)

    final_comp_path = outputs_dir / "final_model_comparison.csv"
    model_pickle_path = models_dir / "final_energy_forecasting_model.pkl"
    features_pickle_path = models_dir / "feature_columns.pkl"

    final_comp.to_csv(final_comp_path, index=False)
    print(f"\nFinal model comparison saved to: {final_comp_path}")
    print(final_comp.to_string(index=False))

    # Save best trained model and feature columns
    joblib.dump(best_model_obj, model_pickle_path)
    joblib.dump(get_feature_columns(), features_pickle_path)

    print(f"\nBest trained model saved to: {model_pickle_path}")
    print(f"Feature columns saved to: {features_pickle_path}")

    return final_comp, best_model_obj


if __name__ == "__main__":
    run_model_evaluation()

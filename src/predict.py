"""
Production Prediction Script for Appliances Energy Prediction.
Loads saved model and feature list to perform predictions on new feature samples.
"""

from pathlib import Path
import pandas as pd
import numpy as np
import joblib


class EnergyPredictor:
    """
    Predictor class wrapping trained model and feature alignment logic.
    """
    def __init__(self, model_path: Path = None, features_path: Path = None):
        project_root = Path(__file__).resolve().parent.parent
        if model_path is None:
            model_path = project_root / "models" / "final_energy_forecasting_model.pkl"
        if features_path is None:
            features_path = project_root / "models" / "feature_columns.pkl"

        print(f"Loading model from: {model_path}")
        self.model = joblib.load(model_path)
        print(f"Loading feature list from: {features_path}")
        self.feature_cols = joblib.load(features_path)

    def predict(self, input_df: pd.DataFrame) -> np.ndarray:
        """
        Validates presence of required features and generates predictions.
        """
        missing_cols = [c for c in self.feature_cols if c not in input_df.columns]
        if missing_cols:
            raise ValueError(f"Missing required feature columns: {missing_cols}")

        X_input = input_df[self.feature_cols]
        predictions = self.model.predict(X_input)
        return predictions


def predict_sample():
    """
    Sample prediction test using last row of feature dataset.
    """
    project_root = Path(__file__).resolve().parent.parent
    features_data_path = project_root / "Data" / "energy_consumption_features.csv"

    if not features_data_path.exists():
        print("Feature dataset not found. Please run feature engineering first.")
        return

    df = pd.read_csv(features_data_path)
    predictor = EnergyPredictor()

    sample_rows = df.tail(5)
    preds = predictor.predict(sample_rows)

    result_df = pd.DataFrame({
        "date": sample_rows["date"].values,
        "actual_Appliances": sample_rows["Appliances"].values,
        "predicted_Appliances": np.round(preds, 2)
    })

    print("\n--- SAMPLE PREDICTIONS ---")
    print(result_df.to_string(index=False))
    return result_df


if __name__ == "__main__":
    predict_sample()

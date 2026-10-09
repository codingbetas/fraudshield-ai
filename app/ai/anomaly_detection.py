"""
Isolation Forest inference.
Returns True if the transaction is an anomaly.
"""

import os
import joblib
import pandas as pd

from app.ai.feature_engineering import build_features, FEATURE_NAMES

MODEL_PATH = os.path.join("model", "anomaly_model.pkl")


if not os.path.exists(MODEL_PATH):
    raise RuntimeError("Anomaly model not found. Run train_model.py first.")

iso_model = joblib.load(MODEL_PATH)


def detect_anomaly(features_dict):
    features = build_features(features_dict)
    df = pd.DataFrame([features], columns=FEATURE_NAMES)
    prediction = iso_model.predict(df)
    return bool(prediction[0] == -1)
import os
import json
import joblib
import numpy as np
import pandas as pd   # ← ADD THIS

from app.ai.feature_engineering import build_features, FEATURE_NAMES

MODEL_PATH = os.path.join("model", "fraud_model.pkl")
METADATA_PATH = os.path.join("model", "MODEL_METADATA.json")


if not os.path.exists(MODEL_PATH):
    raise RuntimeError("Fraud model not found. Run train_model.py first.")

model = joblib.load(MODEL_PATH)


if os.path.exists(METADATA_PATH):
    with open(METADATA_PATH) as f:
        _metadata = json.load(f)
    _expected_features = _metadata.get("feature_names", [])
    if _expected_features and _expected_features != FEATURE_NAMES:
        raise RuntimeError(
            "Feature mismatch: model was trained on different features. "
            "Retrain with train_model.py."
        )


def predict_fraud(features_dict):
    features = build_features(features_dict)
    # Preserve feature names by using a DataFrame
    df = pd.DataFrame([features], columns=FEATURE_NAMES)   # ← CHANGED
    probability = model.predict_proba(df)[0][1]
    return float(probability)
"""
Train Random Forest and Isolation Forest on Kaggle Credit Card Fraud data.

Both models use the same feature vector defined in
app/ai/feature_engineering.py.

Run:
    python train_model.py
"""

import os
import json
import pandas as pd
import joblib
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.metrics import classification_report, roc_auc_score

from app.ai.feature_engineering import FEATURE_NAMES


DATA_PATH = "data/creditcard.csv"
MODEL_DIR = "model"
RANDOM_STATE = 42


def load_and_prepare():
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(
            f"Dataset not found at {DATA_PATH}. "
            "Download from: https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud"
        )

    print("Loading Kaggle Credit Card dataset...")
    df = pd.read_csv(DATA_PATH)

    print(f"Total samples: {len(df)}")
    print(f"Fraud rate: {df['Class'].mean():.4%}")

    X = df[FEATURE_NAMES]
    y = df["Class"].astype(int)

    return X, y


def train_random_forest(X_train, y_train, X_test, y_test):
    print("\nTraining Random Forest...")
    rf = RandomForestClassifier(
        n_estimators=100,
        class_weight="balanced",
        random_state=RANDOM_STATE,
        n_jobs=-1,
    )
    rf.fit(X_train, y_train)

    y_pred = rf.predict(X_test)
    y_proba = rf.predict_proba(X_test)[:, 1]

    print("\nRandom Forest Results:")
    print(classification_report(y_test, y_pred, digits=4))
    print(f"AUC-ROC: {roc_auc_score(y_test, y_proba):.4f}")

    return rf


def train_isolation_forest(X_train, y_train, X_test, y_test):
    print("\nTraining Isolation Forest...")
    X_train_normal = X_train[y_train == 0]

    # Kaggle fraud rate is ~0.17%
    iso = IsolationForest(
        contamination=0.0017,
        random_state=RANDOM_STATE,
        n_jobs=-1,
    )
    iso.fit(X_train_normal)

    iso_pred = iso.predict(X_test)
    iso_anomaly = (iso_pred == -1).astype(int)

    print("\nIsolation Forest Results:")
    print(classification_report(y_test, iso_anomaly, digits=4))

    return iso


def save_metadata():
    metadata = {
        "feature_names": FEATURE_NAMES,
        "dataset": "Kaggle Credit Card Fraud",
        "random_state": RANDOM_STATE,
    }
    path = os.path.join(MODEL_DIR, "MODEL_METADATA.json")
    with open(path, "w") as f:
        json.dump(metadata, f, indent=2)
    print(f"\nSaved metadata: {path}")


def main():
    os.makedirs(MODEL_DIR, exist_ok=True)

    X, y = load_and_prepare()

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=RANDOM_STATE,
        stratify=y,
    )

    rf = train_random_forest(X_train, y_train, X_test, y_test)
    iso = train_isolation_forest(X_train, y_train, X_test, y_test)

    joblib.dump(rf, os.path.join(MODEL_DIR, "fraud_model.pkl"))
    joblib.dump(iso, os.path.join(MODEL_DIR, "anomaly_model.pkl"))
    save_metadata()

    print("\nSaved models:")
    print("  model/fraud_model.pkl")
    print("  model/anomaly_model.pkl")
    print("  model/MODEL_METADATA.json")


if __name__ == "__main__":
    main()
"""
Feature selection: train RF on all 30 features, pick top 8 by importance.

Run once:
    python select_features.py

Then update FEATURE_NAMES in app/ai/feature_engineering.py with the output.
"""

import os
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier

DATA_PATH = "data/creditcard.csv"
N_FEATURES_TO_SELECT = 8

if not os.path.exists(DATA_PATH):
    raise FileNotFoundError(f"Dataset not found at {DATA_PATH}")

print("Loading dataset...")
df = pd.read_csv(DATA_PATH)

print(f"Total samples: {len(df)}")
print(f"Fraud rate: {df['Class'].mean():.4%}")

X = df.drop("Class", axis=1)
y = df["Class"]

print(f"\nTraining Random Forest on {X.shape[1]} features...")
rf = RandomForestClassifier(
    n_estimators=100,
    class_weight="balanced",
    random_state=42,
    n_jobs=-1,
)
rf.fit(X, y)

importances = pd.DataFrame({
    "feature": X.columns,
    "importance": rf.feature_importances_,
}).sort_values("importance", ascending=False)

print("\nAll features ranked by importance:")
print(importances.to_string(index=False))

top = importances.head(N_FEATURES_TO_SELECT)
print(f"\n=== Top {N_FEATURES_TO_SELECT} features ===")
for _, row in top.iterrows():
    print(f"  {row['feature']:12s}  {row['importance']:.6f}")

print("\nCopy this into FEATURE_NAMES in app/ai/feature_engineering.py:")
print(f"FEATURE_NAMES = {list(top['feature'])}")
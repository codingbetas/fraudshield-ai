import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

# Dummy dataset
data = {
    "amount": [1000, 5000, 200, 3000, 7000, 150, 2500, 8000],
    "type": ["TRANSFER", "CASH_OUT", "TRANSFER", "TRANSFER", "CASH_OUT", "PAYMENT", "DEBIT", "TRANSFER"],
    "oldbalanceOrg": [5000, 20000, 1000, 15000, 30000, 500, 12000, 40000],
    "newbalanceOrig": [4000, 15000, 800, 12000, 25000, 350, 9500, 36000],
    "is_fraud": [0, 1, 0, 0, 1, 0, 0, 1]
}

df = pd.DataFrame(data)

# Encode type
type_mapping = {"TRANSFER": 0, "CASH_OUT": 1, "DEBIT": 2, "PAYMENT": 3}
df["type_encoded"] = df["type"].map(type_mapping)

X = df[["amount", "type_encoded", "oldbalanceOrg", "newbalanceOrig"]]
y = df["is_fraud"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save model
os.makedirs("model", exist_ok=True)
joblib.dump(model, "model/fraud_model.pkl")

print("Model trained and saved as model/fraud_model.pkl")

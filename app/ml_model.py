import joblib
import os
import numpy as np

MODEL_PATH = os.path.join("model", "fraud_model.pkl")

# Load model
if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)
else:
    raise Exception("Model not found. Please run train_model.py first.")

def predict_fraud(amount, type, oldbalanceOrg, newbalanceOrig):
    """
    Predict fraud using trained ML model.
    """
    # Simple mapping for type
    type_mapping = {"TRANSFER": 0, "CASH_OUT": 1, "DEBIT": 2, "PAYMENT": 3}
    type_encoded = type_mapping.get(type.upper(), 0)

    features = np.array([[amount, type_encoded, oldbalanceOrg, newbalanceOrig]])
    
    if model:
        pred = model.predict(features)
        return bool(pred[0])
    else:
        # Default fallback if model not trained
        return False

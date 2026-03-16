from app.ai.feature_engineering import create_features
from app.ai.risk_scoring import calculate_risk
from app.ai.anomaly_detection import detect_anomaly
from app.ml_model import predict_fraud

def process_transaction(transaction):

    features = create_features(
        transaction.amount,
        transaction.oldbalanceOrg,
        transaction.newbalanceOrig
    )

    probability = predict_fraud(
        transaction.amount,
        transaction.type,
        transaction.oldbalanceOrg,
        transaction.newbalanceOrig
    )

    risk = calculate_risk(probability)

    anomaly = detect_anomaly(features)

    return {
        "fraud_probability": probability,
        "risk_level": risk,
        "anomaly_detected": anomaly
    }
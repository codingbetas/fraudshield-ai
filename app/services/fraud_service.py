from app.ml_model import predict_fraud
from app.ai.anomaly_detection import detect_anomaly
from app.ai.risk_scoring import calculate_risk
from app.monitoring.model_metrics import update_metrics


def process_transaction(transaction):
    features_dict = transaction.model_dump()

    probability = predict_fraud(features_dict)
    anomaly = detect_anomaly(features_dict)
    risk = calculate_risk(probability)

    update_metrics(probability=probability, anomaly=anomaly)

    return {
        "fraud_probability": round(probability, 4),
        "risk_level": risk,
        "anomaly_detected": anomaly,
    }
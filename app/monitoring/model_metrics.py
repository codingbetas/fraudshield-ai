"""
Metrics backed by Redis.

Shared across FastAPI and all Celery workers.
"""

from app.redis_client import get_redis # or however you connect to Redis


def _key(name: str) -> str:
    return f"metrics:{name}"


def update_metrics(probability: float, anomaly: bool):
    r = get_redis()
    pipe = r.pipeline()
    pipe.incr(_key("total_predictions"))
    if probability > 0.5:
        pipe.incr(_key("fraud_predictions"))
    if anomaly:
        pipe.incr(_key("anomalies_detected"))
    if probability > 0.8:
        pipe.incr(_key("high_risk"))
    elif probability > 0.5:
        pipe.incr(_key("medium_risk"))
    else:
        pipe.incr(_key("low_risk"))
    pipe.execute()


def get_metrics():
    r = get_redis()
    keys = [
        "total_predictions",
        "fraud_predictions",
        "anomalies_detected",
        "high_risk",
        "medium_risk",
        "low_risk",
    ]
    return {
        key: int(r.get(_key(key)) or 0)
        for key in keys
    }
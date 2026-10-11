"""
Tests for the Redis-backed metrics module.

These tests share state with conftest's clean_metrics fixture.
"""

from app.monitoring.model_metrics import update_metrics, get_metrics


def test_metrics_start_at_zero():
    """Fresh metrics (after cleanup) are all zero."""
    metrics = get_metrics()
    assert metrics["total_predictions"] == 0
    assert metrics["fraud_predictions"] == 0
    assert metrics["anomalies_detected"] == 0


def test_update_metrics_increments_total():
    """Every call increments total_predictions."""
    update_metrics(probability=0.1, anomaly=False)
    update_metrics(probability=0.2, anomaly=False)

    metrics = get_metrics()
    assert metrics["total_predictions"] == 2
    assert metrics["fraud_predictions"] == 0
    assert metrics["low_risk"] == 2


def test_update_metrics_fraud_prediction():
    """Probability > 0.5 increments fraud_predictions."""
    update_metrics(probability=0.6, anomaly=False)

    metrics = get_metrics()
    assert metrics["total_predictions"] == 1
    assert metrics["fraud_predictions"] == 1
    assert metrics["medium_risk"] == 1


def test_update_metrics_high_risk():
    """Probability > 0.8 increments high_risk."""
    update_metrics(probability=0.95, anomaly=True)

    metrics = get_metrics()
    assert metrics["high_risk"] == 1
    assert metrics["anomalies_detected"] == 1
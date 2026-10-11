"""
Tests for the FastAPI endpoints.

Because Celery runs in eager mode, tasks execute synchronously.
"""


def test_health(client):
    """The root endpoint returns a health message."""
    response = client.get("/")
    assert response.status_code == 200
    assert "FraudShield AI" in response.json()["message"]


def test_predict_returns_task_id(client, sample_transaction):
    """POST /predict returns a task ID immediately."""
    response = client.post("/predict", json=sample_transaction)
    assert response.status_code == 200

    data = response.json()
    assert "task_id" in data
    assert data["message"] == "Fraud analysis started"


def test_task_result_after_eager_execution(client, sample_transaction):
    """
    In eager mode, the task executes synchronously. We can fetch
    the result immediately and it should contain the expected fields.
    """
    predict_response = client.post("/predict", json=sample_transaction)
    task_id = predict_response.json()["task_id"]

    result_response = client.get(f"/tasks/{task_id}")
    assert result_response.status_code == 200

    data = result_response.json()
    assert data["task_id"] == task_id
    assert data["status"] == "SUCCESS"
    assert "result" in data

    result = data["result"]
    assert "fraud_probability" in result
    assert "risk_level" in result
    assert "anomaly_detected" in result

    assert isinstance(result["fraud_probability"], float)
    assert result["risk_level"] in ("LOW", "MEDIUM", "HIGH")
    assert isinstance(result["anomaly_detected"], bool)


def test_metrics_endpoint_returns_zeros_initially(client):
    """GET /metrics returns all counter keys with zero values."""
    response = client.get("/metrics")
    assert response.status_code == 200

    data = response.json()
    expected_keys = {
        "total_predictions",
        "fraud_predictions",
        "anomalies_detected",
        "high_risk",
        "medium_risk",
        "low_risk",
    }
    assert set(data.keys()) == expected_keys
    assert all(v == 0 for v in data.values())
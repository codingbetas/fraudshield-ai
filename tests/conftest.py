"""
Shared fixtures.

Celery runs in eager mode for tests — tasks execute synchronously
in the same process, so we don't need a running Celery worker.
Redis must still be running for metrics.
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.core.celery_app import celery_app
from app.redis_client import get_redis


@pytest.fixture(scope="session", autouse=True)
def celery_eager_mode():
    original_eager = celery_app.conf.task_always_eager
    original_propagates = celery_app.conf.task_eager_propagates
    original_store = celery_app.conf.task_store_eager_result

    celery_app.conf.task_always_eager = True
    celery_app.conf.task_eager_propagates = True
    celery_app.conf.task_store_eager_result = True

    yield

    celery_app.conf.task_always_eager = original_eager
    celery_app.conf.task_eager_propagates = original_propagates
    celery_app.conf.task_store_eager_result = original_store


@pytest.fixture(scope="function", autouse=True)
def clean_metrics():
    """
    Wipe metrics keys before each test so counters are predictable.
    """
    r = get_redis()
    keys = [
        "metrics:total_predictions",
        "metrics:fraud_predictions",
        "metrics:anomalies_detected",
        "metrics:high_risk",
        "metrics:medium_risk",
        "metrics:low_risk",
    ]
    r.delete(*keys)
    yield
    r.delete(*keys)


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def sample_transaction():
    """
    8 features selected by Random Forest importance.
    """
    return {
        "V14": -0.5,
        "V10": -0.3,
        "V12": -0.4,
        "V4": 0.8,
        "V17": -0.2,
        "V3": 0.5,
        "V11": 0.6,
        "V16": -0.4,
    }
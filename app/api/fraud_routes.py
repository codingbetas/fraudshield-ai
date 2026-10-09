from fastapi import APIRouter
from celery.result import AsyncResult

from app.schemas import TransactionCreate
from app.tasks.fraud_tasks import run_fraud_detection
from app.core.celery_app import celery_app
from app.monitoring.model_metrics import get_metrics

router = APIRouter()


@router.post("/predict")
def predict(transaction: TransactionCreate):
    task = run_fraud_detection.delay(transaction.model_dump())
    return {
        "task_id": task.id,
        "message": "Fraud analysis started",
    }


@router.get("/tasks/{task_id}")
def get_task_result(task_id: str):
    task = AsyncResult(task_id, app=celery_app)
    response = {"task_id": task_id, "status": task.status}
    if task.ready():
        if task.successful():
            response["result"] = task.result
        else:
            response["error"] = str(task.info)
    return response


@router.get("/metrics")
def metrics():
    return get_metrics()
from fastapi import APIRouter
from app.schemas import TransactionCreate
from app.tasks.fraud_tasks import run_fraud_detection

router = APIRouter()

@router.post("/predict")

def predict(transaction: TransactionCreate):

    task = run_fraud_detection.delay(transaction.dict())

    return {
        "task_id": task.id,
        "message": "Fraud analysis started"
    }
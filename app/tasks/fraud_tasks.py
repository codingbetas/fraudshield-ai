from app.schemas import TransactionCreate
from app.core.celery_app import celery_app
from app.services.fraud_service import process_transaction


@celery_app.task(bind=True, max_retries=3)
def run_fraud_detection(self, transaction_data):
    try:
        transaction = TransactionCreate(**transaction_data)
        result = process_transaction(transaction)
        return result
    except Exception as exc:
        raise self.retry(exc=exc, countdown=2 ** self.request.retries)
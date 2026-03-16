from app.schemas import TransactionCreate
from app.core.celery_app import celery_app
from app.services.fraud_service import process_transaction


@celery_app.task
def run_fraud_detection(transaction_data):
    # Convert dict to Pydantic model so .amount, .type etc. work
    transaction = TransactionCreate(**transaction_data)
    
    # Call your existing service function
    result = process_transaction(transaction)
    
    return result
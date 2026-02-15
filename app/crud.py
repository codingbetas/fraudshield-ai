from sqlalchemy.orm import Session
from app.models import Transaction
from app.schemas import TransactionCreate
from app.database import SessionLocal, Base, engine

# Create tables
Base.metadata.create_all(bind=engine)

def create_transaction(transaction: TransactionCreate, is_fraud: bool):
    db = SessionLocal()
    db_transaction = Transaction(
        amount=transaction.amount,
        type=transaction.type,
        oldbalanceOrg=transaction.oldbalanceOrg,
        newbalanceOrig=transaction.newbalanceOrig,
        is_fraud=is_fraud
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    db.close()
    return db_transaction

def get_all_transactions():
    db = SessionLocal()
    transactions = db.query(Transaction).all()
    db.close()
    return transactions

from fastapi import FastAPI, HTTPException
from app.schemas import TransactionCreate, TransactionResponse
from app.crud import create_transaction, get_all_transactions
from app.ml_model import predict_fraud

app = FastAPI(title="FraudShield AI")

@app.get("/")
def root():
    return {"message": "FraudShield AI backend is running 🚀"}

@app.post("/predict", response_model=TransactionResponse)
def predict(transaction: TransactionCreate):
    """
    Predict if a transaction is fraudulent.
    """
    prediction = predict_fraud(transaction.amount, transaction.type, transaction.oldbalanceOrg, transaction.newbalanceOrig)
    db_transaction = create_transaction(transaction, prediction)
    return db_transaction

@app.get("/transactions", response_model=list[TransactionResponse])
def list_transactions():
    """
    List all transactions.
    """
    return get_all_transactions()

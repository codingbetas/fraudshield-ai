from pydantic import BaseModel

class TransactionCreate(BaseModel):
    amount: float
    type: str  # e.g., 'TRANSFER', 'CASH_OUT'
    oldbalanceOrg: float
    newbalanceOrig: float

class TransactionResponse(TransactionCreate):
    id: int
    is_fraud: bool

class Config:
    from_attributes = True


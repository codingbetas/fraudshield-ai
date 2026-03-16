from fastapi import FastAPI
from app.api.fraud_routes import router as fraud_router

app = FastAPI(title="FraudShield AI")

app.include_router(fraud_router)

@app.get("/")
def root():
    return {"message": "FraudShield AI backend is running 🚀"}
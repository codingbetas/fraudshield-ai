# 🚀 FraudShield AI

FraudShield AI is a FastAPI-based backend application that uses Machine Learning models (Random Forest + Isolation Forest) to detect fraudulent financial transactions.

It supports asynchronous transaction processing with Celery + Redis, stores data in a SQLite database, and provides REST API endpoints for prediction and transaction history.

---

## 🧰 Features

- FastAPI backend with REST API endpoints
- Asynchronous processing using Celery + Redis
- Fraud detection using Random Forest & Isolation Forest
- Transaction history stored in SQLite
- Swagger/OpenAPI documentation for easy testing
- Modular code structure for maintainability

---

## ⚡ Setup Instructions

```bash
# Clone the repository
git clone https://github.com/codingbetas/fraudshield-ai.git
cd fraudshield-ai

# Create virtual environment
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Start Redis server
redis-server.exe

# Start Celery worker
celery -A app.core.celery_app worker --loglevel=info

# Train ML model (if not already included)
python app/train_model.py

# Run FastAPI server
uvicorn app.main:app --reload

API will run at: http://127.0.0.1:8000
Swagger Docs: http://127.0.0.1:8000/docs
```

🧪 How to Test the API


1️⃣ Open Swagger UI

Visit:
http://127.0.0.1:8000/docs

2️⃣ Test Fraud Prediction

Click POST /predict → Try it out → Paste the sample JSON:
```
{
  "amount": 5000,
  "type": "TRANSFER",
  "oldbalanceOrg": 20000,
  "newbalanceOrig": 15000
}
```

Click Execute.

You will receive a response like:

{
  "task_id": "02f240c7-a6e1-4c52-bac7-5419e2595397",
  "message": "Fraud analysis started"
}
```

2️⃣a Check Task Result (Optional)
```
If you expose a GET /tasks/{task_id} endpoint, you can query the task status and result using the task ID.

```

🔮 Future Improvements

Add a Next.js frontend dashboard for interactive transaction visualization

Expand ML models for higher fraud detection accuracy

Switch to PostgreSQL or another production-grade database

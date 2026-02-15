# 🚀 FraudShield AI

FraudShield AI is a FastAPI-based backend application that uses a Machine Learning model (Random Forest) to detect fraudulent financial transactions.

It stores transactions in a SQLite database and provides REST API endpoints for prediction and transaction history.


git clone https://github.com/YOUR_USERNAME/fraudshield-ai.git
cd fraudshield-ai

python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate   # Mac/Linux

pip install -r requirements.txt

python app/train_model.py

uvicorn app.main:app --reload

API will run at:
http://127.0.0.1:8000

Swagger Docs:
http://127.0.0.1:8000/docs

---

## 🧪 How to Test the API

### 1️⃣ Open Swagger UI

After running the server, open:

http://127.0.0.1:8000/docs

---

### 2️⃣ Test Fraud Prediction

Click **POST /predict** → Click **Try it out** → Paste this sample JSON:

{
  "amount": 5000,
  "type": "TRANSFER",
  "oldbalanceOrg": 20000,
  "newbalanceOrig": 15000
}

Click **Execute**

You will receive a response like:

{
  "id": 1,
  "amount": 5000,
  "type": "TRANSFER",
  "oldbalanceOrg": 20000,
  "newbalanceOrig": 15000,
  "is_fraud": true
}

---

### 3️⃣ View All Transactions

Open in browser:

http://127.0.0.1:8000/transactions

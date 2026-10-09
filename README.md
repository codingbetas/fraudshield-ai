# 🚀 FraudShield AI

An asynchronous credit card fraud detection backend built with **FastAPI**, **Celery**, **Redis**, and **Scikit-learn**.

FraudShield AI combines supervised machine learning and unsupervised anomaly detection to identify potentially fraudulent credit card transactions. It uses the [Kaggle Credit Card Fraud Detection dataset](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud) containing **284,807 transactions**.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-009688)
![Celery](https://img.shields.io/badge/Celery-37814A)
![Redis](https://img.shields.io/badge/Redis-DC382D)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E)

---

## 📑 Table of Contents

- [Features](#-features)
- [Architecture](#️-architecture)
- [API Endpoints](#-api-endpoints)
- [Model Performance](#-model-performance)
- [Feature Selection](#-feature-selection)
- [API Usage](#-api-usage)
- [Setup and Installation](#️-setup-and-installation)
- [Project Structure](#-project-structure)
- [Production Design](#-production-design)
- [Known Limitations](#️-known-limitations)
- [Future Improvements](#-future-improvements)
- [Dataset](#-dataset)
- [Disclaimer](#️-disclaimer)

---

## ✨ Features

- **FastAPI REST API** — Submit transactions for asynchronous fraud analysis.
- **Celery + Redis** — Process predictions in the background.
- **Dual-model detection** — Combines Random Forest classification with Isolation Forest anomaly detection.
- **Feature selection** — Uses 8 features selected from the original 30 dataset columns.
- **Redis-backed metrics** — Shares prediction counters between the API and Celery workers.
- **SQLite database** — Supports local transaction storage.
- **Swagger/OpenAPI** — Interactive API documentation and testing.

---

## 🏗️ Architecture

```text
                 Client
                   |
                   | POST /predict
                   v
               FastAPI API
             (returns task_id)
                   |
                   | Enqueue task
                   v
             Redis Task Broker
                   |
                   v
              Celery Worker
                   |
            +------+------+
            |             |
            v             v
       Random Forest  Isolation Forest
            |             |
            +------+------+
                   |
                   v
            Risk Assessment
                   |
                   v
           Prediction Result
                   |
                   v
             Celery Backend
```

Redis also stores shared prediction metrics.

---

## 🔌 API Endpoints

| Method | Endpoint           | Description                    |
|--------|--------------------|--------------------------------|
| `POST` | `/predict`         | Submit a prediction task       |
| `GET`  | `/tasks/{task_id}` | Retrieve task status and result |
| `GET`  | `/metrics`         | Retrieve prediction metrics    |
| `GET`  | `/`                | API health check               |

> Redis serves as the Celery broker and stores shared metrics. Task-result retrieval depends on the configured Celery result backend.

---

## 📊 Model Performance

### Random Forest — Supervised Classification

| Metric    | Reported Score |
|-----------|----------------|
| Precision | 0.9744         |
| Recall    | 0.7755         |
| F1-score  | 0.8636         |
| AUC-ROC   | 0.9531         |

### Isolation Forest — Anomaly Detection

| Metric    | Reported Score |
|-----------|----------------|
| Precision | 0.4020         |
| Recall    | 0.8163         |
| F1-score  | 0.5387         |

> **Note:** These are the reported evaluation results for this project. They should be reproduced against a documented evaluation split before being treated as verified model performance.

### Why use two models?

- **Random Forest** — Provides a supervised fraud probability, with relatively high reported precision.
- **Isolation Forest** — Identifies unusual transactions and may flag fraudulent cases that the classifier misses, at the cost of more false positives.

A potential production workflow could send transactions flagged by Isolation Forest but not by Random Forest to a manual-review queue.

> The two outputs are separate signals. A production decision policy should explicitly define how they are combined.

---

## 🎯 Feature Selection

The API accepts the following eight features:

```text
V14, V10, V12, V4, V17, V3, V11, V16
```

They were selected using Random Forest feature importance through `select_features.py`.

Feature selection reduces the API input from 30 columns to 8. Training and inference must use the same feature names, order, and preprocessing.

> ⚠️ **Important:** These are PCA-transformed dataset features, not directly interpretable transaction fields such as merchant name or cardholder identity.

---

## 📡 API Usage

Start the application and open:

| Resource     | URL                              |
|--------------|----------------------------------|
| Swagger UI   | http://127.0.0.1:8000/docs       |
| ReDoc        | http://127.0.0.1:8000/redoc      |
| Health check | http://127.0.0.1:8000/           |

### 1. Submit a prediction

```bash
curl -X POST "http://127.0.0.1:8000/predict" ^
  -H "Content-Type: application/json" ^
  -d "{\"V14\":-1.5,\"V10\":-1.2,\"V12\":-2.0,\"V4\":1.5,\"V17\":-1.8,\"V3\":-1.0,\"V11\":1.2,\"V16\":-0.5}"
```

> The command above uses **Windows Command Prompt** syntax. For PowerShell, use `curl.exe` or submit the JSON through Swagger UI.

Example response:

```json
{
  "task_id": "example-task-id",
  "message": "Fraud analysis started"
}
```

The task ID is used to retrieve the result after background processing. The ID above is illustrative.

### 2. Retrieve the prediction result

Replace the example task ID with the ID returned by `/predict`.

```bash
curl "http://127.0.0.1:8000/tasks/example-task-id"
```

Example response:

```json
{
  "task_id": "example-task-id",
  "status": "SUCCESS",
  "result": {
    "fraud_probability": 0.83,
    "risk_level": "HIGH",
    "anomaly_detected": true
  }
}
```

> This response is illustrative; actual predictions depend on the supplied features and trained models.

### 3. Retrieve prediction metrics

```bash
curl "http://127.0.0.1:8000/metrics"
```

Example response:

```json
{
  "total_predictions": 3,
  "fraud_predictions": 2,
  "anomalies_detected": 2,
  "high_risk": 2,
  "medium_risk": 0,
  "low_risk": 1
}
```

> These values are examples, not live metrics.

---

## ⚙️ Setup and Installation

### Prerequisites

- Python 3.10 or another version supported by your dependencies
- Redis Server
- Git
- pip

### Step 1: Clone the repository

```bash
git clone https://github.com/codingbetas/fraudshield-ai.git
cd fraudshield-ai
```

### Step 2: Create a virtual environment

**Windows Command Prompt**

```bat
python -m venv venv
venv\Scripts\activate
```

**Windows PowerShell**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Linux / macOS**

```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Download the dataset

Download the [Kaggle Credit Card Fraud Detection dataset](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud) and place the CSV file at:

```text
data/creditcard.csv
```

### Step 5: Select features

```bash
python select_features.py
```

This script ranks the original dataset features by Random Forest importance. Ensure that its selected feature list matches `FEATURE_NAMES` in `app/ai/feature_engineering.py` before training.

### Step 6: Train the models

```bash
python train_model.py
```

The training script should generate the following artifacts:

```text
model/
├── fraud_model.pkl
├── anomaly_model.pkl
└── MODEL_METADATA.json
```

### Step 7: Start Redis

If Redis is installed as a Windows executable:

```bash
redis-server.exe
```

Alternatively, use your existing Redis service or Docker instance. Ensure the application's connection settings match the running instance.

### Step 8: Start the Celery worker

Open another terminal, activate the virtual environment, and run:

```bash
celery -A app.core.celery_app worker --loglevel=info --pool=solo
```

> The `solo` pool is useful for local Windows development.

### Step 9: Start FastAPI

Open another terminal, activate the virtual environment, and run:

```bash
uvicorn app.main:app --reload
```

Visit http://127.0.0.1:8000/docs to test the endpoints.

> 🛠️ **Troubleshooting:** If tasks remain pending, check Redis connectivity, the Celery worker logs, and the configured broker and result backend.

---

## 📁 Project Structure

```text
FraudShieldAI/
├── app/
│   ├── ai/
│   │   ├── feature_engineering.py
│   │   ├── anomaly_detection.py
│   │   └── risk_scoring.py
│   ├── api/
│   │   └── fraud_routes.py
│   ├── core/
│   │   └── celery_app.py
│   ├── monitoring/
│   │   └── model_metrics.py
│   ├── services/
│   │   └── fraud_service.py
│   ├── tasks/
│   │   └── fraud_tasks.py
│   ├── crud.py
│   ├── database.py
│   ├── main.py
│   ├── ml_model.py
│   ├── models.py
│   ├── redis_client.py
│   └── schemas.py
├── model/
│   ├── fraud_model.pkl
│   ├── anomaly_model.pkl
│   └── MODEL_METADATA.json
├── select_features.py
├── train_model.py
├── requirements.txt
└── README.md
```

The dataset under `data/` is kept locally and is not required to be committed to Git.

---

## 🔬 Production Design

The current API accepts eight precomputed model features. It demonstrates asynchronous inference, but it is **not** a complete real-world payment ingestion system.

Possible future production improvements include:

- Transaction ingestion and online feature engineering
- A feature store such as Feast
- Durable transaction and prediction storage
- Explicit decision rules combining classifier and anomaly signals
- Data-drift detection and model-quality monitoring
- Structured logging, alerting, authentication, and rate limiting
- Model versioning and reproducible training
- PostgreSQL and database migrations for larger workloads
- Docker Compose for repeatable deployment

Potential technologies include **Kafka** and **Flink** for streaming, **PostgreSQL** for persistent storage, and **Prometheus** with **Grafana** for monitoring.

---

## ⚠️ Known Limitations

- **Anonymized features:** PCA-transformed variables are difficult to interpret.
- **Limited generalization:** The dataset may not represent current fraud patterns across different financial institutions.
- **Class imbalance:** Fraud accounts for approximately 0.173% of the dataset.
- **Threshold sensitivity:** Precision and recall depend on the decision threshold.
- **Evaluation:** Reported metrics need reproducible validation and should not be assumed to describe future performance.
- **Monitoring:** Redis counters are useful for a demonstration but are not a replacement for durable monitoring.
- **Explainability:** Anomaly flags do not automatically explain why a transaction is suspicious.
- **Security:** Production deployments require appropriate authentication, authorization, rate limiting, and secret management.

---

## 🚀 Future Improvements

- [ ] Build a Next.js dashboard for transaction visualization
- [ ] Add data-drift detection and model monitoring
- [ ] Replace SQLite with PostgreSQL and Alembic migrations
- [ ] Add Docker and Docker Compose
- [ ] Expand unit and integration test coverage
- [ ] Integrate Prometheus and Grafana
- [ ] Add structured logging and centralized error handling
- [ ] Implement model versioning and audit logs
- [ ] Introduce configurable risk thresholds and manual-review workflows

---

## 📄 Dataset

This project uses the [Kaggle Credit Card Fraud Detection dataset](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud). Refer to the dataset's terms and documentation for applicable usage conditions.

---

## ⚖️ Disclaimer

FraudShield AI is an educational and experimental project demonstrating asynchronous machine-learning inference and fraud detection.

Its predictions should not be treated as definitive evidence of fraud or used as the sole basis for financial decisions without appropriate validation, monitoring, and human oversight.

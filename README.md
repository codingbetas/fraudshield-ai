🚀 FraudShield AI

An asynchronous credit card fraud detection backend built with FastAPI, Celery, Redis, and Scikit-learn.

FraudShield AI uses supervised machine learning and unsupervised anomaly detection to identify potentially fraudulent credit card transactions.

The models are trained on the Kaggle Credit Card Fraud Detection dataset, which contains 284,807 transactions.

✨ Features
FastAPI REST API — Submit transactions for asynchronous fraud analysis.
Celery + Redis — Process machine learning predictions in the background.
Dual-model detection — Combines Random Forest classification with Isolation Forest anomaly detection.
Feature selection — Uses the top 8 features selected from the original 30 features.
Redis-backed metrics — Shares prediction metrics between the API and Celery workers.
SQLite database — Stores transaction records.
Swagger/OpenAPI documentation — Explore and test endpoints interactively.
🏗️ Architecture
                    ┌──────────────────┐
                    │      Client      │
                    └────────┬─────────┘
                             │
                       POST /predict
                             │
                             ▼
                    ┌──────────────────┐
                    │    FastAPI API   │
                    │                  │
                    │ Returns task_id  │
                    └────────┬─────────┘
                             │
                       Enqueue task
                             │
                             ▼
                    ┌──────────────────┐
                    │      Redis       │
                    │   Task Broker    │
                    └────────┬─────────┘
                             │
                         Consume task
                             │
                             ▼
                    ┌──────────────────┐
                    │  Celery Worker   │
                    │                  │
                    │ ┌──────────────┐ │
                    │ │ Random Forest│ │
                    │ └──────────────┘ │
                    │                  │
                    │ ┌──────────────┐ │
                    │ │Isolation      │ │
                    │ │Forest         │ │
                    │ └──────────────┘ │
                    │                  │
                    │ ┌──────────────┐ │
                    │ │ Metrics      │ │
                    │ │ (Redis)      │ │
                    │ └──────────────┘ │
                    └────────┬─────────┘
                             │
                    Store prediction result
                             │
                             ▼
                    ┌──────────────────┐
                    │   Task Backend   │
                    │  (Configuration  │
                    │    dependent)    │
                    └──────────────────┘

Client endpoints:
  GET /tasks/{task_id}
  GET /metrics
  GET /


Note: Redis serves as the Celery broker and stores shared metrics. The actual Celery result backend depends on your application configuration.

📊 Model Performance
Random Forest — Supervised Classification
Metric	Fraud Class
Precision	0.9744
Recall	0.7755
F1-score	0.8636
AUC-ROC	0.9531
Isolation Forest — Unsupervised Anomaly Detection
Metric	Fraud Class
Precision	0.4020
Recall	0.8163
F1-score	0.5387

These are the reported evaluation results for this project. Actual performance may vary with the evaluation split, preprocessing, and decision thresholds.

Why use two models?

The two models provide complementary signals:

Random Forest: High precision (0.9744), meaning relatively few of its fraud predictions are false positives. Its recall (0.7755) indicates that some fraudulent transactions are missed.
Isolation Forest: Higher recall (0.8163), helping flag more potentially fraudulent transactions, but lower precision (0.4020), resulting in more false positives.

A potential production workflow could send transactions flagged by Isolation Forest but not by Random Forest to a manual review queue.

Important: The models' outputs should be combined through an explicitly defined decision policy rather than assuming that either model's prediction alone establishes fraud.

🎯 Feature Selection

FraudShield AI uses the following eight selected features:

V14, V10, V12, V4, V17, V3, V11, V16


These features are selected based on Random Forest feature importance, reducing the API input from 30 features to 8.

The selection process is implemented in select_features.py.

Important: The feature order, preprocessing, and mapping used during training must match the inference pipeline. Feature importance alone does not guarantee that a feature set will generalize to unseen transactions.

📡 API Endpoints
Method	Endpoint	Description
POST	/predict	Submit a transaction for asynchronous fraud analysis
GET	/tasks/{task_id}	Retrieve the status and result of a prediction task
GET	/metrics	Retrieve prediction metrics
GET	/	Check API health
1. Submit a prediction
curl -X POST "http://127.0.0.1:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "V14": -1.5,
    "V10": -1.2,
    "V12": -2.0,
    "V4": 1.5,
    "V17": -1.8,
    "V3": -1.0,
    "V11": 1.2,
    "V16": -0.5
  }'


Example response:

{
  "task_id": "02f240c7-a6e1-4c52-bac7-5419e2595397",
  "message": "Fraud analysis started"
}


The API returns a task ID so you can retrieve the result after background processing.

2. Retrieve the prediction result
curl "http://127.0.0.1:8000/tasks/02f240c7-a6e1-4c52-bac7-5419e2595397"


Example response:

{
  "task_id": "02f240c7-a6e1-4c52-bac7-5419e2595397",
  "status": "SUCCESS",
  "result": {
    "fraud_probability": 0.83,
    "risk_level": "HIGH",
    "anomaly_detected": true
  }
}


The response above is illustrative. The actual response depends on your implementation and model predictions.

3. Retrieve prediction metrics
curl "http://127.0.0.1:8000/metrics"


Example response:

{
  "total_predictions": 3,
  "fraud_predictions": 2,
  "anomalies_detected": 2,
  "high_risk": 2,
  "medium_risk": 0,
  "low_risk": 1
}


These values are sample output, not live metrics.

4. Open the API documentation

Once the application is running, visit:

Swagger UI: http://127.0.0.1:8000/docs
ReDoc: http://127.0.0.1:8000/redoc
Health check: http://127.0.0.1:8000/
⚙️ Setup and Installation
Prerequisites

Install the following before starting:

Python 3.10 or another version supported by your dependencies
Redis Server
Git
pip
Step 1: Clone the repository
git clone https://github.com/codingbetas/fraudshield-ai.git
cd fraudshield-ai

Step 2: Create a virtual environment

Windows — Command Prompt:

python -m venv venv
venv\Scripts\activate


Windows — PowerShell:

python -m venv venv
.\venv\Scripts\Activate.ps1


Linux/macOS:

python3 -m venv venv
source venv/bin/activate

Step 3: Install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt

Step 4: Download the dataset

Download the Kaggle Credit Card Fraud Detection dataset.

Place the downloaded CSV file at:

data/creditcard.csv


Make sure the data directory exists before placing the file there.

Step 5: Select the features

Run the feature selection script:

python select_features.py


Verify that the script produces the feature metadata or other artifacts expected by your training pipeline.

Step 6: Train the models
python train_model.py


Verify that the trained model files are saved to the expected locations:

model/
├── fraud_model.pkl
├── anomaly_model.pkl
└── MODEL_METADATA.json


The exact output depends on how your training scripts are implemented.

Step 7: Start Redis

If Redis is installed as a Windows executable:

redis-server.exe


If Redis is running as a service or in Docker, use that existing instance instead.

Make sure the Redis connection settings in your application match the running server.

Step 8: Start the Celery worker

Open a new terminal, activate the virtual environment, and run:

celery -A app.core.celery_app worker --loglevel=info --pool=solo


The solo pool is useful for local Windows development. On supported production platforms, a different worker pool may be appropriate.

Step 9: Start the FastAPI server

Open another terminal, activate the virtual environment, and run:

uvicorn app.main:app --reload


The API should now be available at:

http://127.0.0.1:8000


Open the Swagger documentation to test the endpoints:

http://127.0.0.1:8000/docs


Troubleshooting: If predictions remain pending, verify that Redis, the Celery worker, and the API are running and that the Celery broker and result backend settings are configured correctly.

📁 Project Structure
FraudShieldAI/
│
├── data/
│   └── creditcard.csv
│
├── model/
│   ├── fraud_model.pkl
│   ├── anomaly_model.pkl
│   └── MODEL_METADATA.json
│
├── app/
│   ├── main.py
│   ├── schemas.py
│   ├── models.py
│   ├── database.py
│   ├── crud.py
│   ├── ml_model.py
│   ├── redis_client.py
│   │
│   ├── ai/
│   │   ├── feature_engineering.py
│   │   ├── anomaly_detection.py
│   │   └── risk_scoring.py
│   │
│   ├── api/
│   │   └── fraud_routes.py
│   │
│   ├── core/
│   │   └── celery_app.py
│   │
│   ├── services/
│   │   └── fraud_service.py
│   │
│   ├── tasks/
│   │   └── fraud_tasks.py
│   │
│   └── monitoring/
│       └── model_metrics.py
│
├── select_features.py
├── train_model.py
├── requirements.txt
└── README.md

Key components
File or directory	Responsibility
app/main.py	Initializes the FastAPI application
app/schemas.py	Defines request and response schemas
app/database.py	Configures database connectivity
app/crud.py	Handles database operations
app/ml_model.py	Runs Random Forest inference
app/ai/feature_engineering.py	Prepares model input features
app/ai/anomaly_detection.py	Runs Isolation Forest inference
app/ai/risk_scoring.py	Maps prediction scores to risk levels
app/core/celery_app.py	Configures Celery
app/tasks/fraud_tasks.py	Defines background prediction tasks
app/services/fraud_service.py	Coordinates fraud analysis
app/monitoring/model_metrics.py	Tracks prediction metrics
select_features.py	Performs feature importance analysis
train_model.py	Trains and saves the models
🔬 Production Design

The current project accepts eight precomputed features directly through the API. This keeps the model inference pipeline straightforward to test, but it is not a complete real-world transaction ingestion system.

A more complete production architecture could use the following flow:

Transaction ingestion: Receive transaction details such as amount, merchant, timestamp, and payment metadata.
Feature engineering: Generate model features through a streaming or online feature pipeline.
Feature storage: Store and retrieve features using a feature store such as Feast, backed by suitable online storage.
Model inference: Retrieve the appropriate features and evaluate the transaction using the fraud detection models.
Decision orchestration: Combine model outputs, business rules, and risk thresholds.
Result persistence: Store the prediction, risk score, and relevant transaction metadata.
Monitoring: Track latency, prediction quality, data drift, and operational failures.

Possible technologies include Kafka and Flink for streaming, Redis for online data access, PostgreSQL for persistent records, and Prometheus with Grafana for monitoring.

The existing FastAPI, Celery, and Redis architecture provides a starting point for asynchronous inference, but production readiness would require additional reliability, security, and operational controls.

⚠️ Known Limitations
Anonymized features: The dataset uses PCA-transformed features (V1–V28), making individual features difficult to interpret.
Limited generalization: The dataset may not represent fraud patterns across other financial institutions, regions, or time periods.
Class imbalance: Fraud represents approximately 0.173% of the dataset, so evaluation must account for the imbalance.
Threshold sensitivity: Precision and recall can change significantly with the classification threshold.
Evaluation methodology: Performance depends on the train/test split, preprocessing, and validation strategy. Reported metrics should be verified against a reproducible evaluation.
Operational metrics: Redis-backed counters are useful for a demonstration but are not a substitute for durable monitoring and alerting.
SQLite scalability: SQLite is suitable for local development and demos, but PostgreSQL may be a better choice for concurrent production workloads.
Explainability: Anomaly scores and anonymized features do not automatically explain why a transaction is suspicious.
Security: A production API needs authentication, authorization, rate limiting, secure configuration, and appropriate handling of sensitive data.
🚀 Future Improvements
Build a Next.js dashboard for transaction visualization.
Add data drift detection and model performance monitoring.
Replace SQLite with PostgreSQL and Alembic migrations.
Add a Dockerfile and Docker Compose configuration.
Add unit and integration tests for feature engineering, model inference, API routes, and background tasks.
Integrate Prometheus and Grafana for monitoring and alerting.
Add structured logging and centralized error handling.
Implement model versioning and reproducible training.
Add transaction-level explanations and audit logs.
Add configurable risk thresholds and manual review workflows.
📄 Dataset

This project uses the publicly available Kaggle Credit Card Fraud Detection dataset:

https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud

Refer to the dataset's terms and documentation for applicable usage conditions.

⚖️ Disclaimer

FraudShield AI is an educational and experimental project intended to demonstrate asynchronous machine learning inference and fraud detection techniques.

Its predictions should not be treated as definitive evidence of fraud or used as the sole basis for financial decisions without appropriate validation, monitoring, and human oversight.

👨‍💻 Getting Started

Clone the repository, install the dependencies, prepare the dataset, train the models, start Redis and the Celery worker, and launch the FastAPI application.

Then visit http://127.0.0.1:8000/docs to explore the API.
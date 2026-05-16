"""
Churn Prediction API with Axiom Monitoring

Run with:
    litestar --app main:app run --reload
Then open:
    http://localhost:8000/schema/swagger
"""

import time
from litestar import Litestar, get, post
from pydantic import BaseModel

from app.logger_setup import setup_logging, send_to_axiom
from app.model_utils import predict_churn

logger = setup_logging()


# ---------------------------------------------------------------------------
# Request Schema
# ---------------------------------------------------------------------------
class ChurnRequest(BaseModel):
    CreditScore: float
    Geography: str
    Gender: str
    Age: int
    Tenure: float
    Balance: float
    NumOfProducts: int
    HasCrCard: int
    IsActiveMember: int
    EstimatedSalary: float


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@get("/")
async def home() -> dict:
    logger.info("Home endpoint accessed")

    # Send to Axiom
    send_to_axiom({
        "endpoint": "/",
        "method": "GET",
        "event_type": "request",
        "status_code": 200,
    })

    return {"message": "Welcome to the Churn Prediction API!"}


@get("/health")
async def health() -> dict:
    logger.info("Health check endpoint accessed")

    # Send to Axiom
    send_to_axiom({
        "endpoint": "/health",
        "method": "GET",
        "event_type": "request",
        "status_code": 200,
    })

    return {"status": "healthy"}


@post("/predict")
async def predict(data: ChurnRequest) -> dict:
    start_time = time.time()

    features = [
        data.CreditScore,
        data.Geography,
        data.Gender,
        data.Age,
        data.Tenure,
        data.Balance,
        data.NumOfProducts,
        data.HasCrCard,
        data.IsActiveMember,
        data.EstimatedSalary,
    ]

    logger.info(f"Received prediction request with features: {features}")

    # Get prediction
    prediction = predict_churn(features)

    # Calculate response time
    response_time_ms = (time.time() - start_time) * 1000







    # Calculate prediction confidence (probability)
    from app.model_utils import model, transformer
    import pandas as pd
    from app.model_utils import FEATURE_COLUMNS

    df = pd.DataFrame([features], columns=FEATURE_COLUMNS)
    features_transformed = transformer.transform(df)
    probabilities = model.predict_proba(features_transformed)[0]
    confidence = float(max(probabilities))
    churn_probability = float(probabilities[1])  # probability of churn=1

    logger.info(f"Prediction result: {prediction}, confidence: {confidence}")

    # ── Detect out-of-range features ──
    invalid_input = False
    if not (300 <= data.CreditScore <= 850):
        invalid_input = True
    if not (18 <= data.Age <= 100):
        invalid_input = True
    if not (0 <= data.Tenure <= 10):
        invalid_input = True
    if data.NumOfProducts not in [1, 2, 3, 4]:
        invalid_input = True

    # ── Send rich event to Axiom ──
    send_to_axiom({
        # Server metrics
        "event_type": "prediction",
        "endpoint": "/predict",
        "method": "POST",
        "status_code": 201,
        "response_time_ms": round(response_time_ms, 2),

        # Model metrics
        "predicted_class": prediction,
        "churn_probability": round(churn_probability, 4),
        "prediction_confidence": round(confidence, 4),
        "predicted_label": "churn" if prediction == 1 else "no_churn",

        # Data metrics
        "credit_score": data.CreditScore,
        "age": data.Age,
        "tenure": data.Tenure,
        "balance": data.Balance,
        "num_of_products": data.NumOfProducts,
        "geography": data.Geography,
        "gender": data.Gender,
        "estimated_salary": data.EstimatedSalary,
        "has_cr_card": data.HasCrCard,
        "is_active_member": data.IsActiveMember,
        "invalid_input": invalid_input,
    })

    return {
        "churn_prediction": prediction,
        "churn_probability": round(churn_probability, 4),
        "confidence": round(confidence, 4),
    }


# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------
app = Litestar(
    route_handlers=[home, health, predict],
)
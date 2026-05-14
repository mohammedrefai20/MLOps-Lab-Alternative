"""
Tests for the Churn Prediction API.

Run with:
    pytest tests/ -v
    pytest tests/ -v --cov=app --cov=main --cov-report=term-missing
"""
import pytest
from litestar.testing import TestClient

from app.model_utils import predict_churn
from main import app


SAMPLE_FEATURES = [
    620.0,    # CreditScore
    "France", # Geography
    "Male",   # Gender
    42,       # Age
    2.0,      # Tenure
    10000.0,  # Balance
    1,        # NumOfProducts
    1,        # HasCrCard
    1,        # IsActiveMember
    50000.0,  # EstimatedSalary
]

SAMPLE_JSON = {
    "CreditScore": 620.0,
    "Geography": "France",
    "Gender": "Male",
    "Age": 42,
    "Tenure": 2.0,
    "Balance": 10000.0,
    "NumOfProducts": 1,
    "HasCrCard": 1,
    "IsActiveMember": 1,
    "EstimatedSalary": 50000.0,
}


# ---------------------------------------------------------------------------
# Function Tests
# ---------------------------------------------------------------------------

# TODO 1: Write a test that calls predict_churn() directly with sample features
#         and asserts the result is 0 or 1
#         Hint: import predict_churn from app.model_utils
def test_predict_churn_returns_valid_prediction():
    result = predict_churn(SAMPLE_FEATURES)
    assert isinstance(result, int)
    assert result in (0, 1)

# TODO 2 (bonus): Write another function test with edge-case inputs
def test_predict_churn_edge_case_zero_balance():
    edge_features = [
        850.0,    # CreditScore (max)
        "Spain",  # Geography
        "Female", # Gender
        18,       # Age (minimum adult)
        0.0,      # Tenure
        0.0,      # Balance (zero)
        1,        # NumOfProducts
        0,        # HasCrCard
        0,        # IsActiveMember
        10000.0,  # EstimatedSalary
    ]
    result = predict_churn(edge_features)
    assert isinstance(result, int)
    assert result in (0, 1)

# ---------------------------------------------------------------------------
# Endpoint Tests
# ---------------------------------------------------------------------------

# TODO 3: Write a test that POSTs to /predict with valid JSON
#         and checks the status code and response body
#         Hint: Litestar POST returns 201, not 200
#         Hint: use `with TestClient(app=app) as client:`

def test_predict_endpoint():
    with TestClient(app=app) as client:
        response = client.post("/predict", json=SAMPLE_JSON)
        assert response.status_code == 201
        body = response.json()
        assert "churn_prediction" in body
        assert body["churn_prediction"] in (0, 1)

# TODO 4: Write a test for GET /health
def test_health_endpoint():
    with TestClient(app=app) as client:
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}


# TODO 5: Write a test for GET /
def test_home_endpoint():
    with TestClient(app=app) as client:
        response = client.get("/")
        assert response.status_code == 200
        body = response.json()
        assert "message" in body


# TODO 6 (bonus): Test that invalid input returns status 400
def test_predict_endpoint_invalid_input():
    with TestClient(app=app) as client:
        invalid_payload = {
            "CreditScore": "not_a_number",  # wrong type
            "Geography": "France",
            "Gender": "Male",
            "Age": "old",                   # wrong type
            "Tenure": 2.0,
            "Balance": 10000.0,
            "NumOfProducts": 1,
            "HasCrCard": 1,
            "IsActiveMember": 1,
            "EstimatedSalary": 50000.0,
        }
        response = client.post("/predict", json=invalid_payload)
        assert response.status_code == 400
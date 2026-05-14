"""
Model loading and prediction logic.

The model must be loaded ONCE at module level, NOT inside the predict function.
"""
import joblib
import pandas as pd

# TODO 1: Load your serialized churn model from data/model.joblib
model = joblib.load('data/model.pkl')
transformer = joblib.load('data/column_transformer.joblib')
FEATURE_COLUMNS = [
    "CreditScore",
    "Geography",
    "Gender",
    "Age",
    "Tenure",
    "Balance",
    "NumOfProducts",
    "HasCrCard",
    "IsActiveMember",
    "EstimatedSalary",
]

def predict_churn(features: list[float]) -> int:
    """
    Takes a list of feature values and returns a churn prediction (0 or 1).
    """
    # TODO 2: Use model.predict() to get a prediction and return it as an int
    #         Hint: model.predict() expects a 2D array
    df = pd.DataFrame([features], columns=FEATURE_COLUMNS)
    features_transformed = transformer.transform(df)
    prediction = model.predict(features_transformed)
    return int(prediction[0])


if __name__ == "__main__":
    # TODO 3: Replace with sample features that match your model
    sample = [
        620.0,   # CreditScore
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
    
    print(f"Input:      {sample}")
    print(f"Prediction: {predict_churn(sample)}")

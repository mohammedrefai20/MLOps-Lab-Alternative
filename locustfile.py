from locust import HttpUser, task, between


class ChurnAPIUser(HttpUser):
    # Each simulated user waits 1-3 seconds between requests
    # This simulates realistic human behavior
    wait_time = between(1, 3)

    @task(1)
    def home(self):
        """Test GET / endpoint"""
        self.client.get("/")

    @task(1)
    def health(self):
        """Test GET /health endpoint"""
        self.client.get("/health")

    @task(3)
    def predict(self):
        """Test POST /predict endpoint — weighted 3x more than others"""
        payload = {
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
        self.client.post("/predict", json=payload)
# Locust tests are implemented here
from locust import HttpUser, task, between

class MyUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def submit_data(self):
        self.client.post("/submit", json={"transaction_id": "12345",
        "user_id": "67890",
        "amount": 100.0,
        "currency": "USD",
        "timestamp": "2024-08-31T12:34:56"
})

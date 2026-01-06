from locust import HttpUser, task, between
import random

class EmailUser(HttpUser):
    wait_time = between(0.01, 0.1)  # small wait → high load

    @task
    def generate_email(self):
        payload = {
            "candidate_name": "Sooraj Aryan",
            "recipient_email": "test@example.com",
            "recipient_name": "HR",
            "recipient_position": "Backend Engineer",
            "company_name": "TestCorp",
            "company_location": "Bangalore",
            "resume_text": "Python, FastAPI, AI projects"
        }

        self.client.post("/generate-email", json=payload)

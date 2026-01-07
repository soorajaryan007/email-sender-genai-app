from locust import HttpUser, task, between
import random

class EmailUser(HttpUser):
    wait_time = between(1, 3)

    @task(3)
    def generate_email(self):
        payload = {
            "recipient_email": "test@example.com",
            "recipient_name": "John Doe",
            "recipient_position": "Hiring Manager",
            "company_name": "Acme Corp",
            "company_location": "Bangalore",
            "resume_text": "Experienced Python and FastAPI developer with ML background.",
            "candidate_name": "Sooraj Aryan"
        }

        with self.client.post(
            "/generate-email",
            json=payload,
            catch_response=True,
            timeout=60
        ) as response:
            if response.status_code != 200:
                response.failure("Generate email failed")

    @task(1)
    def send_email(self):
        payload = {
            "email_id": "dummy-id",
            "to_email": "receiver@example.com",
            "subject": "Test Email",
            "edited_body": "This is a test email body."
        }

        with self.client.post(
            "/send-email",
            json=payload,
            catch_response=True,
            timeout=30
        ) as response:
            if response.status_code != 200:
                response.failure("Send email failed")

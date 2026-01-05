import os
import smtplib
from email.mime.text import MIMEText


def send_email(to_email: str, subject: str, body: str):
    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = os.getenv("SMTP_PORT")
    smtp_email = os.getenv("SMTP_EMAIL")
    smtp_password = os.getenv("SMTP_PASSWORD")

    if not all([smtp_host, smtp_port, smtp_email, smtp_password]):
        raise RuntimeError("SMTP configuration missing in environment")

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = smtp_email
    msg["To"] = to_email

    with smtplib.SMTP_SSL(smtp_host, int(smtp_port)) as server:
        server.login(smtp_email, smtp_password)
        server.send_message(msg)

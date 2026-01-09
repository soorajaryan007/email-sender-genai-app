import os
import smtplib
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from typing import Optional


def send_email(
    to_email: str, 
    subject: str, 
    body: str,
    attachment_filename: Optional[str] = None,
    attachment_content: Optional[str] = None
):
    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = os.getenv("SMTP_PORT")
    smtp_email = os.getenv("SMTP_EMAIL")
    smtp_password = os.getenv("SMTP_PASSWORD")

    if not all([smtp_host, smtp_port, smtp_email, smtp_password]):
        raise RuntimeError("SMTP configuration missing in environment")

    # Create multipart message if attachment exists
    if attachment_filename and attachment_content:
        msg = MIMEMultipart()
        msg.attach(MIMEText(body, 'plain'))
        
        # Decode base64 attachment
        try:
            pdf_data = base64.b64decode(attachment_content)
            pdf_attachment = MIMEApplication(pdf_data, _subtype='pdf')
            pdf_attachment.add_header(
                'Content-Disposition', 
                'attachment', 
                filename=attachment_filename
            )
            msg.attach(pdf_attachment)
        except Exception as e:
            raise RuntimeError(f"Failed to process attachment: {str(e)}")
    else:
        msg = MIMEText(body)

    msg["Subject"] = subject
    msg["From"] = smtp_email
    msg["To"] = to_email

    with smtplib.SMTP_SSL(smtp_host, int(smtp_port)) as server:
        server.login(smtp_email, smtp_password)
        server.send_message(msg)
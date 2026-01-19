import smtplib
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from typing import Optional
from groq import Groq
from django.conf import settings


class GroqService:
    """Handle LLM interactions"""
    
    def __init__(self):
        self.client = Groq(api_key=settings.GROQ_API_KEY)
    
    def generate_cold_email(self, prompt: str, model: Optional[str] = None) -> str:
        """Generate cold email using Groq API"""
        system_prompt = """You are a professional email writer.Do not include subject line.I will include it.
        write an email to hiring manager according to Candidate Resume and Recipient Details.
        Make it concise and engaging.
        Include Candidate Name in the email.
        Generate a professional cold email under 150 words."""
        
        try:
            response = self.client.chat.completions.create(
                model=model or settings.GROQ_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt},
                ],
                temperature=settings.GROQ_TEMPERATURE,
                max_tokens=settings.GROQ_MAX_TOKENS,
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            raise RuntimeError(f"Groq generation failed: {str(e)}")


class EmailService:
    """Handle email sending"""
    
    @staticmethod
    def send_email(
        to_email: str,
        subject: str,
        body: str,
        attachment_filename: Optional[str] = None,
        attachment_content: Optional[str] = None
    ):
        """Send email via SMTP"""
        smtp_host = settings.SMTP_HOST
        smtp_port = settings.SMTP_PORT
        smtp_email = settings.SMTP_EMAIL
        smtp_password = settings.SMTP_PASSWORD
        
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
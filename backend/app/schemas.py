from pydantic import BaseModel, EmailStr, field_validator


class EmailRequest(BaseModel):
    recipient_email: EmailStr
    recipient_name: str
    recipient_position: str
    company_name: str
    company_location: str
    resume_text: str
    candidate_name: str


class SendEmailRequest(BaseModel):
    email_id: str
    to_email: str
    subject: str
    edited_body: str

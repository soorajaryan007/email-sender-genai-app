from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv

from app.schemas import EmailRequest
from app.llm import generate_cold_email
from app.store import save_email,get_email_body
from app.email_service import send_email
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vue dev server
        "http://localhost:8080",
        "http://127.0.0.1:8080", 
        "*",
    ],

    allow_credentials=True,
    allow_methods=["*"],        # POST, GET, OPTIONS, etc.
    allow_headers=["*"],
)


@app.post("/generate-email")
def generate_email(data: EmailRequest):
    prompt = f"""
Candidate Resume:{data.resume_text}
Candidate Name:{data.candidate_name}

Recipient Details:
Name: {data.recipient_name}
Position: {data.recipient_position}
Company: {data.company_name}
Location: {data.company_location}
"""

    email_body = generate_cold_email(prompt)

    # ✅ STORE GENERATED EMAIL,Emailaddress,
    email_id = save_email(email_body)

    return {
        "email_id": email_id,
        "recipient_email": data.recipient_email,
        "email_body": email_body
    }



@app.post("/send-email")
def send_generated_email(
    email_id: str,
    to_email: str,
    subject: str
):
    email_body = get_email_body(email_id)

    if not email_body:
        raise HTTPException(status_code=404, detail="Generated email not found")

    send_email(
        to_email=to_email,
        subject=subject,
        body=email_body  # ✅ GENERATED EMAIL BODY USED HERE
    )

    return {
        "status": "Email sent successfully",
        "email_id": email_id
    }

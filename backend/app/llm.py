from groq import Groq
from app.config import settings
from typing import Optional

# Create client once (connection reuse)
client = Groq(api_key=settings.groq_api_key)


def generate_cold_email(
    prompt: str,
    model: Optional[str] = None,
) -> str:

    system_prompt = """You are a professional email writer.Do not include subject line.I will include it.
    write an email to hiring manager according to Candidate Resume and Recipient Details.
    Make it concise and engaging.
    Include Candidate Name in the email.
    Generate a professional cold email under 150 words."""

    try:
        response = client.chat.completions.create(
            model=model or settings.groq_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            temperature=settings.groq_temperature,
            max_tokens=settings.groq_max_tokens,
        )

        return response.choices[0].message.content

    except Exception as e:
        # Log in real apps
        raise RuntimeError(f"Groq generation failed: {str(e)}")


from typing import Dict
from uuid import uuid4

EMAIL_STORE: Dict[str, str] = {}


def save_email(content: str,) -> str:
    # 🔥 Clear old data to save memory
    #EMAIL_STORE.clear()

    email_id = str(uuid4())
    EMAIL_STORE[email_id] = content


    return email_id


def get_email_body(email_id: str) -> str | None:
    return EMAIL_STORE.get(email_id)

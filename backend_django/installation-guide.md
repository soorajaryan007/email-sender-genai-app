# Django Cold Email Generator - Setup Guide

## Project Structure

```
cold_email_generator/
├── cold_email_generator/
│   ├── __init__.py
│   ├── settings.py          # Main settings (artifact provided)
│   ├── urls.py              # Project URLs (see urls.py artifact)
│   ├── wsgi.py
│   └── asgi.py
├── emails/                   # Django app
│   ├── __init__.py
│   ├── models.py            # Database models (artifact provided)
│   ├── views.py             # API views (artifact provided)
│   ├── serializers.py       # DRF serializers (artifact provided)
│   ├── services.py          # Business logic (artifact provided)
│   ├── urls.py              # App URLs (artifact provided)
│   ├── admin.py
│   └── migrations/
├── manage.py
├── requirements.txt         # Dependencies (artifact provided)
└── .env                     # Environment variables
```

## Setup Instructions

### 1. Create Django Project

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Django
pip install django

# Create project
django-admin startproject cold_email_generator
cd cold_email_generator

# Create app
python manage.py startapp emails
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the project root:

```env
# Django
DJANGO_SECRET_KEY=your-secret-key-here
APP_ENV=development

# Groq API
GROQ_API_KEY=your-groq-api-key
GROQ_MODEL=llama-3.3-70b-versatile
GROQ_TEMPERATURE=0.4
GROQ_MAX_TOKENS=1024

# SMTP Configuration
SMTP_HOST=smtp.gmail.com
SMTP_PORT=465
SMTP_EMAIL=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

### 4. Copy Artifacts to Project Files

Replace/create the following files with the provided artifacts:
- `cold_email_generator/settings.py`
- `emails/models.py`
- `emails/serializers.py`
- `emails/services.py`
- `emails/views.py`
- `emails/urls.py`

### 5. Update Project URLs

Edit `cold_email_generator/urls.py`:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('emails.urls')),
]
```

### 6. Register Models in Admin (Optional)

Edit `emails/admin.py`:

```python
from django.contrib import admin
from .models import GeneratedEmail, SentEmail

@admin.register(GeneratedEmail)
class GeneratedEmailAdmin(admin.ModelAdmin):
    list_display = ['email_id', 'recipient_name', 'company_name', 'created_at']
    search_fields = ['recipient_name', 'company_name']
    readonly_fields = ['email_id', 'created_at']

@admin.register(SentEmail)
class SentEmailAdmin(admin.ModelAdmin):
    list_display = ['to_email', 'subject', 'sent_at']
    search_fields = ['to_email', 'subject']
```

### 7. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 8. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 9. Run Development Server

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/`

## API Endpoints

### 1. Generate Email
**POST** `/generate-email`

Request body:
```json
{
  "recipient_email": "hiring@company.com",
  "recipient_name": "John Doe",
  "recipient_position": "Hiring Manager",
  "company_name": "Tech Corp",
  "company_location": "San Francisco, CA",
  "resume_text": "Full resume text here...",
  "candidate_name": "Jane Smith"
}
```

Response:
```json
{
  "email_id": "uuid-here",
  "recipient_email": "hiring@company.com",
  "email_body": "Generated email content..."
}
```

### 2. Send Email
**POST** `/send-email`

Request body:
```json
{
  "email_id": "uuid-from-generation",
  "to_email": "hiring@company.com",
  "subject": "Application for Software Engineer Position",
  "edited_body": "Email content (can be edited)",
  "attachment_filename": "resume.pdf",
  "attachment_content": "base64-encoded-pdf-content"
}
```

Response:
```json
{
  "status": "Email sent successfully",
  "email_id": "uuid-here"
}
```

## Key Differences from FastAPI Version

1. **Database Storage**: Uses Django ORM with SQLite (easily switchable to PostgreSQL/MySQL) instead of in-memory dictionary
2. **Models**: Proper database models for `GeneratedEmail` and `SentEmail`
3. **Admin Interface**: Built-in admin panel at `/admin/` for managing data
4. **Migrations**: Database schema versioning with Django migrations
5. **DRF Integration**: Uses Django REST Framework for API views and serialization
6. **CORS**: Handled via `django-cors-headers` middleware
7. **Settings**: Django-style settings configuration instead of Pydantic

## Production Considerations

1. **Database**: Switch to PostgreSQL in production
2. **Secret Key**: Generate a secure `DJANGO_SECRET_KEY`
3. **Debug Mode**: Set `DEBUG=False` in production
4. **Allowed Hosts**: Configure `ALLOWED_HOSTS` properly
5. **Static Files**: Configure static file serving
6. **WSGI Server**: Use Gunicorn or uWSGI instead of development server
7. **Async Support**: Consider using ASGI with Daphne for async LLM calls

## Testing the API

```bash
# Generate email
curl -X POST http://localhost:8000/generate-email \
  -H "Content-Type: application/json" \
  -d '{
    "recipient_email": "test@example.com",
    "recipient_name": "Test User",
    "recipient_position": "Manager",
    "company_name": "Test Co",
    "company_location": "NYC",
    "resume_text": "Sample resume",
    "candidate_name": "John"
  }'

# Send email
curl -X POST http://localhost:8000/send-email \
  -H "Content-Type: application/json" \
  -d '{
    "email_id": "uuid-from-previous-response",
    "to_email": "test@example.com",
    "subject": "Test Subject",
    "edited_body": "Email body here"
  }'
```
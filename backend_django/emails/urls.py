# emails/urls.py (app-level URLs)
from django.urls import path
from .views import GenerateEmailView, SendEmailView

app_name = 'emails'

urlpatterns = [
    path('generate-email', GenerateEmailView.as_view(), name='generate-email'),
    path('send-email', SendEmailView.as_view(), name='send-email'),
]


# cold_email_generator/urls.py (project-level URLs)
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('emails.urls')),
]
"""
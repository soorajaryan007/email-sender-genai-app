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
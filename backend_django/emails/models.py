from django.db import models
import uuid


class GeneratedEmail(models.Model):
    """Store generated emails"""
    email_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email_body = models.TextField()
    recipient_email = models.EmailField(null=True, blank=True)
    recipient_name = models.CharField(max_length=255, null=True, blank=True)
    company_name = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Email {self.email_id} - {self.created_at}"


class SentEmail(models.Model):
    """Track sent emails"""
    generated_email = models.ForeignKey(
        GeneratedEmail, 
        on_delete=models.CASCADE,
        related_name='sent_emails'
    )
    to_email = models.EmailField()
    subject = models.CharField(max_length=500)
    sent_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-sent_at']
    
    def __str__(self):
        return f"Sent to {self.to_email} at {self.sent_at}"
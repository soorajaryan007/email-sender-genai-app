from rest_framework import serializers
from .models import GeneratedEmail, SentEmail


class EmailRequestSerializer(serializers.Serializer):
    recipient_email = serializers.EmailField()
    recipient_name = serializers.CharField(max_length=255)
    recipient_position = serializers.CharField(max_length=255)
    company_name = serializers.CharField(max_length=255)
    company_location = serializers.CharField(max_length=255)
    resume_text = serializers.CharField()
    candidate_name = serializers.CharField(max_length=255)


class SendEmailRequestSerializer(serializers.Serializer):
    email_id = serializers.UUIDField()
    to_email = serializers.EmailField()
    subject = serializers.CharField(max_length=500)
    edited_body = serializers.CharField()
    attachment_filename = serializers.CharField(max_length=255, required=False, allow_null=True)
    attachment_content = serializers.CharField(required=False, allow_null=True)  # base64


class GeneratedEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneratedEmail
        fields = ['email_id', 'email_body', 'recipient_email', 'recipient_name', 
                  'company_name', 'created_at']
        read_only_fields = ['email_id', 'created_at']
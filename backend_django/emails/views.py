from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
import asyncio
from asgiref.sync import sync_to_async

from .serializers import (
    EmailRequestSerializer,
    SendEmailRequestSerializer,
    GeneratedEmailSerializer
)
from .models import GeneratedEmail, SentEmail
from .services import GroqService, EmailService


class GenerateEmailView(APIView):
    """Generate cold email using LLM"""
    
    def post(self, request):
        serializer = EmailRequestSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        
        data = serializer.validated_data
        
        # Build prompt
        prompt = f"""
Candidate Resume:{data['resume_text']}
Candidate Name:{data['candidate_name']}

Recipient Details:
Name: {data['recipient_name']}
Position: {data['recipient_position']}
Company: {data['company_name']}
Location: {data['company_location']}
"""
        
        try:
            # Generate email using Groq
            groq_service = GroqService()
            email_body = groq_service.generate_cold_email(prompt)
            
            # Save to database
            generated_email = GeneratedEmail.objects.create(
                email_body=email_body,
                recipient_email=data['recipient_email'],
                recipient_name=data['recipient_name'],
                company_name=data['company_name']
            )
            
            return Response({
                'email_id': str(generated_email.email_id),
                'recipient_email': data['recipient_email'],
                'email_body': email_body
            }, status=status.HTTP_201_CREATED)
        
        except RuntimeError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            return Response(
                {'error': f'Unexpected error: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class SendEmailView(APIView):
    """Send generated email"""
    
    def post(self, request):
        serializer = SendEmailRequestSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        
        data = serializer.validated_data
        
        try:
            # Verify email exists
            generated_email = GeneratedEmail.objects.get(
                email_id=data['email_id']
            )
            
            # Send email
            EmailService.send_email(
                to_email=data['to_email'],
                subject=data['subject'],
                body=data['edited_body'],
                attachment_filename=data.get('attachment_filename'),
                attachment_content=data.get('attachment_content')
            )
            
            # Track sent email
            SentEmail.objects.create(
                generated_email=generated_email,
                to_email=data['to_email'],
                subject=data['subject']
            )
            
            return Response({
                'status': 'Email sent successfully',
                'email_id': str(data['email_id'])
            }, status=status.HTTP_200_OK)
        
        except ObjectDoesNotExist:
            return Response(
                {'error': 'Email not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except RuntimeError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            return Response(
                {'error': f'Failed to send email: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
from django.shortcuts import render
from django.http import JsonResponse
import uuid
from .models import APIDoc
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from django.core.mail import send_mail

def generate(req):
    return render(req, 'generate.html')

def generateKey():
    return uuid.uuid4().hex[:16]  # Adjusted to generate a 32-character API key

def has_active_api_keys(email):
    # Custom logic to check for active API keys associated with the email
    active_api_docs = APIDoc.objects.filter(username=email, is_active=True)
    if active_api_docs.exists():
        payload = list(active_api_docs.values())  # Convert QuerySet to list of dictionaries
        return True, payload
    return False, None

def genekey(req):
    if req.method == 'POST':
        email = req.POST.get('email')
        
        # Check if there are active API keys for the given email
        has_active_keys, payload = has_active_api_keys(email)
        if has_active_keys:
            return JsonResponse({'message': 'You already have an active API key', 'api_key_data': payload}, status=400)
        
        # Generate a new API key
        apiKey = generateKey()
        
        # Save the new API key in the database
        ins = APIDoc(username=email, api_key=apiKey)
        ins.save()
        subject="MadCoder's Fraud API Key"
        mes=f'Hi Developer, thanks for choosing Madcoder`s api your API key \n Key : {apiKey}'
        fromm=settings.EMAIL_HOST_USER
        recipient = [email,]
        send_mail(subject,mes,fromm,recipient)
        
        return JsonResponse({"apiKey": apiKey, "message": "Success"})
    
    return JsonResponse({"message": "Invalid request method"}, status=405)

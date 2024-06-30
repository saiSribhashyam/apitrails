from django.shortcuts import render
from django.http import JsonResponse
import uuid
from .models import APIDoc
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from django.core.mail import send_mail
import requests

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
        
        subject="MadCoder's Fraud API Key"
        mes=f'Hi Developer, thanks for choosing Madcoder`s api your API key \nKey : {apiKey}'
        fromm=settings.EMAIL_HOST_USER
        recipient = [email,]
        send_mail(subject,mes,fromm,recipient)
        ins.save()
        
        return JsonResponse({"apiKey": apiKey, "message": "Success"})
    
    return JsonResponse({"message": "Invalid request method"}, status=405)

def check_api_key(req, api_key):
    if req.method == 'GET':
        try:
            api_doc = APIDoc.objects.get(api_key=api_key, is_active=True)
        except APIDoc.DoesNotExist:
            return JsonResponse({'message': 'Invalid or inactive API key'}, status=403)

        message = req.GET.get('message', '')
        if not message:
            return JsonResponse({'message': 'No message provided'}, status=400)

        # Call the closed-source service
        response = requests.get(
            'https://mcfraud.onrender.com/',
            params={'message': message}
        )

        if response.status_code == 200:
            data = response.json()
            result = {
                'error': data.get('error', ''),
                'message': data.get('message', ''),
                'predict': data.get('predict', ''),
                'predict_proba': data.get('predict_proba', [])
            }
        else:
            result = {
                'error': 'Failed to get prediction from the service',
                'message': message,
                'predict': '',
                'predict_proba': []
            }

        api_doc.request_count += 1
        api_doc.save()

        return JsonResponse(result)

    return JsonResponse({"message": "Invalid request method"}, status=405)
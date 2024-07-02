from django.shortcuts import render
import requests


# Create your views here.
def index(req):
    return render(req, "index.html")

def fraud(req):
    message = req.POST.get("message")
    if message:
        params = get_fraudResults(message=message)
        params['message'] = message
    else:
        params = {}
    return render(req, "index.html", params)

def test(req):
    params = {"name": "hari"}
    return render(req, "test.html", params)

def get_fraudResults(message):
    api_url = f"https://mcfraud-agc2eegceshphydj.southindia-01.azurewebsites.net/?message={message}"
    response = requests.get(api_url)
    data = response.json()
    return data

def docs(req):
    return render(req,"documentation.html")


def about(req):
    return render(req,"about.html")
# genkey/views.py
from django.shortcuts import render, redirect

def generate(req):
    return render(req, 'generate.html')

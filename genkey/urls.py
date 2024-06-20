# genkey/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('genkey', views.generate, name="generate")
]

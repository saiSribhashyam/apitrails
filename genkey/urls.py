# genkey/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('genkey', views.generate, name="generate"), #genkey redirection for generate api key page
    path('genekey',views.genekey,name="genekey") #function for generating api key along with email
]

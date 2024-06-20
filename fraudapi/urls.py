from django.urls import path
from . import views

urlpatterns=[
    path('',views.index,name="home"),
    path('check', views.fraud,name="fraud"),
    path('test',views.test,name='test'),
    path('api-docs',views.docs,name='api-docs')
]

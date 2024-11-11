from django.urls import path
from barbershop.client import client_view
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register_client', client_view.register_client, name='register_client'),

   
]

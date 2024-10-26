from django.urls import path
from chatbot import views

urlpatterns = [
    path('bot_message/', views.bot_message, name='bot_message'),
 
]

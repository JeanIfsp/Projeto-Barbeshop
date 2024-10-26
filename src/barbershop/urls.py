from django.urls import path, include


urlpatterns = [
    path('schedule/', include('barbershop.urls_schedule')),
    path('service/', include('barbershop.urls_service')),
    path('appointment/', include('barbershop.urls_appointment')),
    path('report/', include('barbershop.url_report')),
]

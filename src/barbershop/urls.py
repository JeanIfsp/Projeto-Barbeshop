from django.urls import path, include


urlpatterns = [
    path('schedule/', include('barbershop.schedule.urls_schedule')),
    path('service/', include('barbershop.service.urls_service')),
    path('appointment/', include('barbershop.appointment.urls_appointment')),
    path('report/', include('barbershop.report.url_report')),
]

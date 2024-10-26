from django.urls import path
from barbershop import appointment_views

urlpatterns = [   
    path('register_appointment', appointment_views.register_appointment, name='register_appointment'),
    path('', appointment_views.list_appointment, name='list_appointment'),
    path('delete_appointment/<int:id>', appointment_views.delete_appointment, name='delete_appointment'),
    path('finish_appointment/<int:id>', appointment_views.finish_appointment, name='finish_appointment'),
    path('reschedule_appointment/<int:id>', appointment_views.reschedule_appointment, name='reschedule_appointment'),
    path('hours_list', appointment_views.hours_list, name='hours_list'),
    path('search_list_appointment/', appointment_views.search_list_appointment, name='search_list_appointment'),
    
]

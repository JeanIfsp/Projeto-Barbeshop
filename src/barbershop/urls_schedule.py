from django.urls import path
from barbershop import schedule_views

urlpatterns = [   
    path('list_schedule', schedule_views.list_schedule, name='list_schedule'),
    path('register_schedule', schedule_views.register_schedule, name='register_schedule'),
    path('update_schedule/<int:id>', schedule_views.update_schedule, name='update_schedule'),
    path('delete_schedule/<int:id>', schedule_views.delete_schedule, name='delete_schedule'),
]

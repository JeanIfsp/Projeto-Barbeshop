from django.urls import path
from barbershop.service import service_views 

urlpatterns = [   
    path('list_service', service_views.list_service, name='list_service'),
    path('register_service', service_views.register_service, name='register_service'),
    path('update_service/<int:id>', service_views.update_service, name='update_service'),
    path('delete_service/<int:id>', service_views.delete_service, name='delete_service'),
    
]

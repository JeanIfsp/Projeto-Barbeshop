from django.urls import path
from barbershop.report import report_view

urlpatterns = [
    path('report', report_view.report, name='report'),
    path('recover_data/', report_view.recover_data, name='recover_data'),
    path('report_week/', report_view.report_week, name='report_week'),
    path('report_week/recover_data_week/', report_view.recover_data_week, name='recover_data_week'),
    path('report_amount/', report_view.report_amount, name='report_amount'),
    path('report_amount/recover_data_amount/', report_view.recover_data_amount, name='recover_data_amount'),
    
    
]

from barbershop.models import Appointment
from barbershop.query import BarbershopService
from barbershop.choices import AppointmentType
from django.db.models import Sum, F, Count
from django.db.models.functions import ExtractWeekDay, TruncDate

class ServiceReport:

    def get_clients(self, user):
        
        return BarbershopService.get_client_list_by_admin_barbeshop(user)

    def get_all_appointment(self, user):
        
        clients_ids = self.get_clients(user)
   
        return Appointment.objects.annotate(
            month=F('date_time__month')
        ).filter(
            user_id__in=clients_ids,
            status=AppointmentType.COMPLETED
        ).values('month', 'type_id__service_type').annotate(
            total_cuts=Count('id'),
        ).order_by('month', 'type_id__service_type')
    

    def get_data_by_type_id(self, type_id, user):

        clients_ids = self.get_clients(user)

        return Appointment.objects.annotate(
            month=F('date_time__month')  
        ).filter(
            type_id=type_id,
            user_id__in=clients_ids,
            status=AppointmentType.COMPLETED
        ).values(
            'month', 'type_id__service_type'  
        ).annotate(
            total_cuts=Count('id'), 
        ).order_by('month', 'type_id__service_type')

    
    def get_data_by_month_number(self, month_number, user):

        clients_ids = self.get_clients(user)

        return Appointment.objects.annotate(
            month=F('date_time__month')  
        ).filter(
            month=month_number,
            user_id__in=clients_ids,
            status=AppointmentType.COMPLETED
        ).values(
            'month', 'type_id__service_type'  
        ).annotate(
            total_cuts=Count('id'), 
        ).order_by('month', 'type_id__service_type')
    
    def get_data_by_month_number_and_type_id(self, month_number, type_id, user):

        clients_ids = self.get_clients(user)

        return Appointment.objects.annotate(
            month=F('date_time__month')  
        ).filter(
            month=month_number,
            type_id=type_id,
            user_id__in=clients_ids,
            status=AppointmentType.COMPLETED
        ).values(
            'month', 'type_id__service_type'  
        ).annotate(
            total_cuts=Count('id'), 
        ).order_by('month', 'type_id__service_type')
    
    
    def get_data_by_week(self, start_date, end_date, type_id, user):

        clients_ids = self.get_clients(user)

        return Appointment.objects.filter(
            date_time__date__gte=start_date,
            date_time__date__lte=end_date,
            type_id=type_id,
            user_id__in=clients_ids,
            status=AppointmentType.COMPLETED
        ).annotate(
            weekday=ExtractWeekDay('date_time'),
            day_month=TruncDate('date_time') 
        ).values(
            'weekday', 'day_month', 'type_id__service_type'
        ).annotate(
            total_cuts=Count('id'),
        ).order_by(
            'day_month', 'type_id__service_type'
        )

    def get_all_amount(self, user):
        
        clients_ids = self.get_clients(user)

        return Appointment.objects.annotate(
            month=F('date_time__month')
        ).filter(
            user_id__in=clients_ids,
            status=AppointmentType.COMPLETED
        ).values('month', 'type_id__service_type').annotate(
            total_price=Sum(F('type_id__price'))
        ).order_by('month', 'type_id__service_type')

    def get_data_by_type_id_amount(self, type_id, user):

        clients_ids = self.get_clients(user)

        return Appointment.objects.annotate(
            month=F('date_time__month')  
        ).filter(
            type_id=type_id,
            user_id__in=clients_ids,
            status=AppointmentType.COMPLETED
        ).values(
            'month', 'type_id__service_type'  
        ).annotate(
            total_cuts=Sum(F('type_id__price')), 
        ).order_by('month', 'type_id__service_type')
    
    
    def get_data_by_month_number_amount(self, month_number, user):

        clients_ids = self.get_clients(user)

        return Appointment.objects.annotate(
            month=F('date_time__month')  
        ).filter(
            month=month_number,
            user_id__in=clients_ids,
            status=AppointmentType.COMPLETED
        ).values(
            'month', 'type_id__service_type'  
        ).annotate(
            total_cuts=Sum(F('type_id__price')), 
        ).order_by('month', 'type_id__service_type')
    
    def get_data_by_month_number_and_type_id_amount(self, month_number, type_id, user):

        clients_ids = self.get_clients(user)

        return Appointment.objects.annotate(
            month=F('date_time__month')  
        ).filter(
            month=month_number,
            type_id=type_id,
            user_id__in=clients_ids,
            status=AppointmentType.COMPLETED
        ).values(
            'month', 'type_id__service_type'  
        ).annotate(
            total_cuts=Sum(F('type_id__price')),
        ).order_by('month', 'type_id__service_type')
    
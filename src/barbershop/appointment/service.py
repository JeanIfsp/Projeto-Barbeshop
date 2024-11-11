import locale
from django.db.models import F
from datetime import datetime, date
from accounts.services import UserService
from barbershop.models import Appointment
from barbershop.choices import AppointmentType
from barbershop.query import BarbershopService
from django.db.models.functions import Extract


class ServiceAppointment:
    
    @staticmethod
    def create_new_appointment(cliend_id, instance,  date_time):

        appointment = Appointment.objects.create(user_id=cliend_id, date_time=date_time, type_id=instance)
        appointment.save()

    def get_appointment_id(self, id):
         
        return Appointment.objects.get(id=id)
    
    def get_saved_month_appointment(request):

        return Appointment.objects.annotate(
            month=F('date_time__month')
        ).values('month').distinct().order_by('month')

        
    def get_appointment_today(self, admin):

        clients_ids = BarbershopService.get_client_list_by_admin_barbeshop(admin)
        today = date.today()
        return Appointment.objects.filter(date_time__date=today, user_id__in=clients_ids).order_by('-id')
    
    def get_appointment_date(self, date, user):

        selected_date = datetime.strptime(date, '%Y-%m-%d').date()
     
        clients_ids = BarbershopService.get_client_list_by_admin_barbeshop(user)
        appointments = Appointment.objects.filter(user_id__in=clients_ids, date_time__date=selected_date).select_related('user', 'type_id')
        return appointments
    
    def get_appointment_user(self, user):

        instance_user = UserService()
        return Appointment.objects.filter(user=instance_user.get_user(user))

    def get_hours_has_status_canceled(self, new_date_time, client_id):
    
        return Appointment.objects.filter(user_id=client_id, date_time=new_date_time, status=AppointmentType.CANCELED).exists()
    
    def get_instance_appointment_id(self, id):

        return Appointment.objects.get(id=id)

    def delete_appointment(self, id):

        instance = self.get_instance_appointment_id(id)
        instance.status = AppointmentType.CANCELED
        instance.save()
    
    def finish_appointment(self, id):

        instance = self.get_instance_appointment_id(id)
        instance.status = AppointmentType.COMPLETED
        instance.save()

    @staticmethod
    def get_appointment_any_day(user, day):
        
        return list(Appointment.objects.filter(date_time__date=day,
                                               type_id__user_id=user.id, 
                                               status__in=(AppointmentType.SHEDULED, AppointmentType.COMPLETED)
                                               ).annotate(hora=Extract('date_time', 'hour')
                                                ).values_list('hora', flat=True))
    
    def update_appointment(self, id, day, instance_service):

        instance = self.get_appointment_id(id)
        instance.date_time = day
        instance.type_id = instance_service 
        instance.save()

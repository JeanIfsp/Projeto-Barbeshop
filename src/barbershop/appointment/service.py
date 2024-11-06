import locale
from django.db.models import F
from datetime import datetime, date
from accounts.services import UserService
from barbershop.models import Appointment
from barbershop.choices import AppointmentType
from django.db.models.functions import Extract


class ServiceAppointment:
    
    @staticmethod
    def create_new_appointment(user, instance,  date_time):

        appointment = Appointment.objects.create(user=user, date_time=date_time, type_id=instance)
        appointment.save()

    def get_appointment_id(self, id):
         
        return Appointment.objects.get(id=id)
    
    def get_saved_month_appointment(request):

        return Appointment.objects.annotate(
            month=F('date_time__month')
        ).values('month').distinct().order_by('month')

        
    def get_appointment_today(self):
        
        today = date.today()
        return Appointment.objects.filter(date_time__date=today)
    
    def get_appointment_date(self, date):
        selected_date = datetime.strptime(date, '%Y-%m-%d').date()
        return  Appointment.objects.filter(date_time__date=selected_date).order_by('-id')
    
    def get_appointment_user(self, user):

        instance_user = UserService()
        return Appointment.objects.filter(user=instance_user.get_user(user))

    def get_hours_has_status_canceled(self, new_date_time):
    
        return Appointment.objects.filter(date_time=new_date_time,status=AppointmentType.CANCELED).exists()
    
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
    def get_appointment_any_day(day):
        
        return list(Appointment.objects.filter(date_time__date=day, status__in=(AppointmentType.SHEDULED, AppointmentType.COMPLETED)).annotate(hora=Extract('date_time', 'hour')).values_list('hora', flat=True))
    
    def update_appointment(self, id, day, instance_service):

        instance = self.get_appointment_id(id)
        instance.date_time = day
        instance.type_id = instance_service 
        instance.save()

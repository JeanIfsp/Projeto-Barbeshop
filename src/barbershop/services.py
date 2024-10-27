from accounts.services import UserService
from barbershop.models import Schedules, Service, Appointment
from barbershop.choices import WeekType, AppointmentType
from datetime import date
from django.db.models.functions import Extract, ExtractWeekDay, TruncDate, TruncMonth
from django.db.models import Sum, F, Count
from datetime import datetime
import locale  



class ShedulesService:
    
    def get_list_shedules(self) -> Schedules:

        return Schedules.objects.all()
    
    def get_list_services_and_prices(self):

        return Service.objects.all()
    
    def get_days_not_registers(self):
   
        day_register = Schedules.objects.values_list('day', flat=True)
        portuguese_days = [day.label.upper() for day in WeekType]
        day_that_is_not_on_the_schedule = (set(portuguese_days) - set(list(day_register)))
        return list(day_that_is_not_on_the_schedule)
    
    def get_hours_day(self, id):

        return Schedules.objects.get(id=id)
    @staticmethod
    def get_hours_by_day_name_week(day):

        return Schedules.objects.get(day__iexact=day)
    
    def create_new_scheduler(self, data):

        day = data.POST.get('day')
        start_work = data.POST.get('start_work')
        end_work = data.POST.get('end_work')
        launch_time = data.POST.get('launch_time')

        schedules = Schedules.objects.create(day=day, start_time=start_work, end_time=end_work, launch_time=int(launch_time))
        schedules.save()
    
    def update_schedule(self, instance, data):

        start_work = data.POST.get('start_work')
        end_work = data.POST.get('end_work')
        instance.start_time=start_work
        instance.end_time=end_work
        instance.save()

    def delete_schedule(self, id):
        
        instance = self.get_hours_day(id)
        instance.delete()
    

class ServicePrice:

    def get_list_service(self) -> Service:

        return Service.objects.all()
    
    @staticmethod
    def get_list_service_name() -> Service:

        return Service.objects.values_list('service_type', flat=True)
    
    def get_list_service_register(self) -> Service:
         
        return Service.objects.values('id', 'service_type').distinct().order_by('id')

    def get_hairname_price_day(self, id):

        return Service.objects.get(id=id)
    
    def get_instace_service_name(self, type_service):
     
        return Service.objects.get(service_type=type_service)
    
    def create_new_scheduler(self, data):

        haircut_name = (data.POST.get('haircut_name'))
        haircut_price = data.POST.get('haircut_price')

        haircut_price = haircut_price.replace(",", ".") if "," in haircut_price else haircut_price 

        schedules = Service.objects.create(service_type=haircut_name.upper(), price=float(haircut_price))
        schedules.save()
    
    def get_haircut_name_to_check(self, data):

        haircut_name = data.POST.get('haircut_name')
        return Service.objects.filter(service_type__iexact=haircut_name.upper()).exists()
    
    def update_service(self, instance, data):

        haircut_name = data.POST.get('haircut_name')
        haircut_price = data.POST.get('haircut_price')
    
        instance.service_type =  haircut_name
        instance.price = float(haircut_price)
        instance.save()

    def delete_service(self, id):
        
        instance = self.get_hairname_price_day(id)
        instance.delete()

class ServiceAppointment:
    
    def create_new_appointment(self, user, instance,  date_time):

        appointment = Appointment.objects.create(user=user, date_time=date_time, type_id=instance)
        appointment.save()

    def get_appointment_id(self, id):
         
        return Appointment.objects.get(id=id)
    
    def get_saved_month_appointment(request):

        locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')

        return Appointment.objects.annotate(
            month=F('date_time__month')
        ).values('month').distinct().order_by('month')

        
    def get_appointment_today(self):
        
        today = date.today()
        return Appointment.objects.filter(date_time__date=today)
    
    def get_appointment_date(self, date):
        selected_date = datetime.strptime(date, '%Y-%m-%d').date()
        return  Appointment.objects.filter(date_time__date=selected_date)
    
    def get_appointment_user(self, user):

        instance_user = UserService()
        return Appointment.objects.filter(user=instance_user.get_user(user))

    def deltatime_created_new_appointmnet(self, new_date_time):
    
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

class ServiceReport:

    def get_all_appointment(self):
        
        return Appointment.objects.annotate(
            month=F('date_time__month')
        ).values('month', 'type_id__service_type').annotate(
            total_cuts=Count('id'),
            total_age=Count('user__age')
        ).order_by('month', 'type_id__service_type')
    

    def get_data_by_type_id(self, type_id):

        return Appointment.objects.annotate(
            month=F('date_time__month')  
        ).filter(
            type_id=type_id
        ).values(
            'month', 'type_id__service_type'  
        ).annotate(
            total_cuts=Count('id'), 
        ).order_by('month', 'type_id__service_type')

    
    def get_data_by_month_number(self, month_number):

        return Appointment.objects.annotate(
            month=F('date_time__month')  
        ).filter(
            month=month_number
        ).values(
            'month', 'type_id__service_type'  
        ).annotate(
            total_cuts=Count('id'), 
        ).order_by('month', 'type_id__service_type')
    
    def get_data_by_month_number_nad_type_id(self, month_number, type_id):

        return Appointment.objects.annotate(
            month=F('date_time__month')  
        ).filter(
            month=month_number,
            type_id=type_id
        ).values(
            'month', 'type_id__service_type'  
        ).annotate(
            total_cuts=Count('id'), 
        ).order_by('month', 'type_id__service_type')
    
    
    def get_data_by_week(self, start_date, end_date, type_id):

        return Appointment.objects.filter(
            date_time__date__gte=start_date,
            date_time__date__lte=end_date,
            type_id=type_id
        ).annotate(
            weekday=ExtractWeekDay('date_time'),
            day_month=TruncDate('date_time') 
        ).values(
            'weekday', 'day_month', 'type_id__service_type'
        ).annotate(
            total_cuts=Count('id'),
            total_age=Count('user__age') 
        ).order_by(
            'day_month', 'type_id__service_type'
        )

    def get_all_amount(self):

        return Appointment.objects.annotate(
            month=F('date_time__month')
        ).values('month', 'type_id__service_type').annotate(
            total_price=Sum(F('type_id__price'))
        ).order_by('month', 'type_id__service_type')

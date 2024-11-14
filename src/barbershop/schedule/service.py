from barbershop.models import Schedules, Service
from barbershop.choices import  WeekType

class ShedulesService:
    
    def get_list_shedules(self, user) -> Schedules:

        return Schedules.objects.filter(user_id=user.id).all()
    
    def get_list_services_and_prices(self):

        return Service.objects.all()
    
    def get_days_not_registers(self, user):
   
        day_register = Schedules.objects.filter(user_id=user.id).values_list('day', flat=True)
        portuguese_days = [day.label.upper() for day in WeekType]
        day_that_is_not_on_the_schedule = (set(portuguese_days) - set(list(day_register)))
        return list(day_that_is_not_on_the_schedule)
    
    def get_hours_day(self, id):

        return Schedules.objects.get(id=id)

    @staticmethod
    def get_hours_by_day_name_week(day, user):
        
        return Schedules.objects.get(day__iexact=day, user_id=user)
    
    def get_hours_by_day_name_week_exists(day, user):

        return Schedules.objects.filter(day__iexact=day, user_id=user).exists()

    def create_new_scheduler(self, data):

        day = data.POST.get('day')
        start_work = data.POST.get('start_work')
        end_work = data.POST.get('end_work')
        launch_time = data.POST.get('launch_time')

        schedules = Schedules.objects.create(day=day, start_time=start_work, end_time=end_work, launch_time=int(launch_time), user=data.user)
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
    
from barbershop.models import Service
from accounts.services import UserService

class ServicePrice:

    @staticmethod
    def get_list_service(user) -> Service:

        return Service.objects.filter(user_id=user.id).all()
    
    @staticmethod
    def get_list_service_name(user) -> Service:

        return Service.objects.filter(user_id=user).values_list('service_type', flat=True)
    
    def get_list_service_register(self, admin) -> Service:
         
        return Service.objects.filter(user_id=admin.id).values('id', 'service_type').distinct().order_by('id')

    def get_hairname_price_day(self, id):

        return Service.objects.get(id=id)
    
    @staticmethod
    def get_instace_service_name(type_service, user):
     
        return Service.objects.get(service_type=type_service, user_id=user)
    
    def create_new_scheduler(self, data):

        haircut_name = (data.POST.get('haircut_name'))
        haircut_price = data.POST.get('haircut_price')

        haircut_price = haircut_price.replace(",", ".") if "," in haircut_price else haircut_price 
        

        schedules = Service.objects.create(service_type=haircut_name.upper(), price=float(haircut_price), user=data.user)
        schedules.save()
    
    def get_haircut_name_to_check(self, data):

        haircut_name = data.POST.get('haircut_name')
        return Service.objects.filter(service_type__iexact=haircut_name.upper(), user_id=data.user.id).exists()
    
    def update_service(self, instance, data):

        haircut_price = data.POST.get('haircut_price')

        haircut_price = haircut_price.replace(",", ".") if "," in haircut_price else haircut_price 

        instance.price = float(haircut_price)
        instance.save()

    def delete_service(self, id):
        
        instance = self.get_hairname_price_day(id)
        instance.delete()
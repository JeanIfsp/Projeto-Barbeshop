from barbershop.models import Service

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
    
    @staticmethod
    def get_instace_service_name(type_service):
     
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

        haircut_price = data.POST.get('haircut_price')

        haircut_price = haircut_price.replace(",", ".") if "," in haircut_price else haircut_price 

        instance.price = float(haircut_price)
        instance.save()

    def delete_service(self, id):
        
        instance = self.get_hairname_price_day(id)
        instance.delete()
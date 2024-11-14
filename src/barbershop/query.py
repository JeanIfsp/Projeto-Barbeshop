from barbershop.models import Barbershop, ClientBarbershop

class BarbershopService:

    @staticmethod
    def create_new_barbershop(user, name_barbershop, address):

        try:
            barbershop = Barbershop.objects.create(admin=user,
                                    name_barbershop=name_barbershop,
                                    address=address
                                    )
            return barbershop
        except Exception as error:
            raise Exception(str(error))
    
    def get_client_by_email_barbeshop(user):
        client_names = ClientBarbershop.objects.filter(admin_id=user).values('client__id','client__client_name')
        return client_names
    
    
    def get_client_list_by_admin_barbeshop(admin):
        clients_ids = ClientBarbershop.objects.filter(admin_id=admin).values_list('client_id', flat=True)
        return clients_ids
    
    @staticmethod
    def get_data_barbershop():
        barbershops = Barbershop.objects.all()
        return barbershops

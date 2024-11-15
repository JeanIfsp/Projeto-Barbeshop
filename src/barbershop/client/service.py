from barbershop.models import Client, ClientBarbershop
from .exception import ServiceClientException

class ClientService:

    @staticmethod
    def create_new_client(data) -> ClientBarbershop:
            
        try:

            cell_phone = data.get("cell_phone_number")
            client_name= data.get("client_name")

            address = data.gte("address") if 'addres' in data else ""
            client = Client.objects.create(client_name=client_name,
                                            cell_phone_number=cell_phone, 
                                            address=address)
            return client
        
        except Exception as error:
            raise False
        except Client.DoesNotExist as error:
            raise ServiceClientException(error)

    def create_relationship_between_cliente_and_barbershop(admin, client) -> ClientBarbershop:

        try:
            
            client_babershop = ClientBarbershop.objects.create(admin=admin, client=client)
            return client_babershop
            
        except Exception as error:
            raise Exception(str(error))
    
    @staticmethod
    def create_relationship_between_cliente_and_barbershop_pass_id(admin, client) -> ClientBarbershop:

        try:
            
            client_babershop = ClientBarbershop.objects.create(admin_id=admin, client_id=client)
            return client_babershop
            
        except Exception as error:
            return False

    @staticmethod
    def get_relationship_between_cliente_and_barbershop_pass_id(admin, client) -> ClientBarbershop:

        try:
            
            client_babershop = ClientBarbershop.objects.filter(admin_id=admin, client_id=client).exists()
            return client_babershop
            
        except Exception as error:
            return False
    
    def get_client_cell_phone_number_exists(cell_phone_number):

        try:
            client = Client.objects.get(cell_phone_number=cell_phone_number)
            return True if client else False
        except Client.DoesNotExist:
            return False
            
    def get_client_cell_phone_number(cell_phone_number):

        try:
            client = Client.objects.get(cell_phone_number=cell_phone_number)
            return client
        except Client.DoesNotExist:
            return None
            
         
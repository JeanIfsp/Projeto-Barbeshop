from barbershop.models import Client, ClientBarbershop

class ClientService:

    @staticmethod
    def create_new_client(data) -> ClientBarbershop:
            
        try:
            print(data)    
            cell_phone = data.get("cell_phone_number")
            client_name= data.get("client_name")

            address = data.gte("address") if 'addres' in data else ""
            client = Client.objects.create(client_name=client_name,
                                            cell_phone_number=cell_phone, 
                                            address=address)
            return client
        
        except Exception as error:
            raise Exception(str(error))

    def create_relationship_between_cliente_and_barbershop(admin, client) -> ClientBarbershop:

        try:
            
            client_babershop = ClientBarbershop.objects.create(admin=admin, client=client)
            return client_babershop
            
        except Exception as error:
            raise Exception(str(error))
         
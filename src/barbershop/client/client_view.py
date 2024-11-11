from django.contrib import messages
from django.shortcuts import render, redirect
from django.db import transaction
from accounts import validator
from accounts import exception
from barbershop.client.service import ClientService


def register_client(request):

    if request.method == "POST":
        
        try:

            cell_phone_number = validator.validator_cell_phone_number(request.POST.get('cell_phone'))
            client_name = validator.validator_barbeshop_name(request.POST.get('client_name'))

            with transaction.atomic(): 
                
                client = ClientService.create_new_client({"cell_phone_number":cell_phone_number,
                                                "client_name":client_name})

                if not client:
                    messages.error("Não foi possível criar o cadastro do cliente")
                
                relationship_client_babrbershop = ClientService.create_relationship_between_cliente_and_barbershop(request.user, client)
                
                if not relationship_client_babrbershop:
                    messages.error("Não foi possível realizar o cadastro do cliente ao estabelecimento")
                messages.success(request, 'Cadastro Realizado com Sucesso!')
                return redirect('register_appointment')

        except exception.ValidationException as error:
            messages.error(request, str(error))
        except exception.ServiceUserException as error:
            messages.error(request, str(error))
        except Exception as error:
            messages.error(request, "Informe outro úmero por gentileza")
    
    return render(request, "clientTemplates/register_client.html")
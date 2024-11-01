from django.shortcuts import render, redirect
from django.urls import reverse
from barbershop.service.service import ServicePrice
from barbershop.permissions import admin_required
from barbershop.service.validator import validate_update_service_price
from django.contrib import messages
import traceback

@admin_required
def list_service(request):

    try:
        
        service_price = ServicePrice()
        service =  service_price.get_list_service()

        if len(service) == 0:

            return redirect(reverse('register_service'))
        
        return render(request, 'servicesTemplates/list_service.html', {'services': service})
    
    except Exception as error:
        messages.ERROR(request, "Ocorreu para listar os serviços")
    finally:
        return render(request, 'servicesTemplates/list_service.html', {'services': service})


def register_service(request):
    
    
    try:
        
        services = ServicePrice()

        if request.method == "POST":

            name_service_exist = services.get_haircut_name_to_check(request)
 
            if name_service_exist:
                messages.error(request, f"O serviço {request.POST.get('haircut_name')} se econtra cadastrado")
                return render(request, 'servicesTemplates/register_service.html')
            
            haircut_price = request.POST.get('haircut_price')
            validate_update_service_price(haircut_price)
            
            services.create_new_scheduler(request)
            return redirect(reverse('list_service'))
        
        return render(request, 'servicesTemplates/register_service.html')
    
    except Exception as error:
        messages.error(request, "Ocorreu algum erro ao registrar novo serviço")
    except ValueError as error:
        print(str(error))
        messages.error(request, str(error))
   
    return render(request, 'servicesTemplates/register_service.html')


def update_service(request, id):

    service = ServicePrice()

    try:
        
        instance_service = service.get_hairname_price_day(id)
        print("instance_service: ", instance_service)
        if request.method == "POST":

            haircut_price = request.POST.get('haircut_price')
            validate_update_service_price(haircut_price)

            service.update_service(instance_service, request)
            return redirect(reverse('list_service'))  
        
        if service is None:
            return redirect(reverse('list_service'))
        
        return render(request,'servicesTemplates/update_service.html', {'services': instance_service})
    except Exception as error:
        print(str(error))
        print(traceback.format_exc())
        messages.error(request, "Ocorreu um erro ao precessar a atualização do do serviço")
    except ValueError as error:
        print(str(error))
        messages.error(request, str(error))
   
    return render(request,'servicesTemplates/update_service.html', {'services': instance_service})


def delete_service(request, id):

    service = ServicePrice()

    try:
        if request.method == "POST":

            service.delete_service(id)
            
            return redirect(reverse('list_service'))
        return redirect(reverse('list_service'))
    except Exception as error:
        messages.ERROR(request, "Error ao deletar dado")
    finally:
        return redirect(reverse('list_service'))

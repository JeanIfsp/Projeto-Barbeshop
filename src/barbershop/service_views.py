from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from barbershop.services import ServicePrice
from barbershop.permissions import admin_required
from django.contrib import messages

@admin_required
def list_service(request):

    try:
        
        service_price = ServicePrice()
        service =  service_price.get_list_service()

        if len(service) == 0:

            return redirect(reverse('register_service'))
        
        return render(request, 'servicesTemplates/list_service.html', {'services': service})
    
    except Exception as error:
        print(str(error))



def register_service(request):
    
    
    try:
        
        services = ServicePrice()

        if request.method == "POST":

            name_service_exist = services.get_haircut_name_to_check(request)
 
            if name_service_exist:
                messages.error(request, f"O serviço {request.POST.get('haircut_name')} se econtra cadastrado")
                return render(request, 'servicesTemplates/register_service.html')
            
            services.create_new_scheduler(request)
            return redirect(reverse('list_service'))
        
        return render(request, 'servicesTemplates/register_service.html')
    
    
    except Exception as error:
        print(error)




def update_service(request, id):

    service = ServicePrice()

    try:
        
        instance_service = service.get_hairname_price_day(id)
        
        if request.method == "POST":

            service.update_service(instance_service, request)
            return redirect(reverse('list_service'))  
        
        if service is None:
            return redirect(reverse('list_service'))
        
        return render(request,'servicesTemplates/update_service.html', {'services': instance_service})
    except Exception as error:
        print(error)


def delete_service(request, id):

    service = ServicePrice()

    try:
        if request.method == "POST":

            service.delete_service(id)
            
            return redirect(reverse('list_service'))
        return redirect(reverse('list_service'))
    except Exception as error:
        print(str(error))

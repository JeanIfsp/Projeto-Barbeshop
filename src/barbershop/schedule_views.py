from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from barbershop.services import ShedulesService
from barbershop.permissions import admin_required
from django.urls import reverse


@admin_required
def list_schedule(request):

    try:
        
        services = ShedulesService()
        schedule =  services.get_list_shedules()

        if len(schedule) == 0:

            return redirect(reverse('register_schedule'))
        
        return render(request, 'scheduleTemplates/list_scheduler.html', {'schedules': schedule})
    
    except Exception as error:
        print(str(error))

@admin_required
def register_schedule(request):
    
    
    try:
        
        services = ShedulesService()

        if request.method == "POST":

            services.create_new_scheduler(request)
            return redirect(reverse('list_schedule'))
        
        days = services.get_days_not_registers()
        return render(request, 'scheduleTemplates/register_schedule.html', {'days': days})
    
    except Exception as error:
        print(error)


@admin_required
def update_schedule(request, id):

    service = ShedulesService()

    try:

        schedule = service.get_hours_day(id)
        
        if request.method == "POST":
            service.update_schedule(schedule, request)
            return redirect(reverse('list_schedule'))  
        if schedule is None:
            return redirect(reverse('list_schedule'))
        return render(request,'scheduleTemplates/update_schedule.html', {"schedule":schedule})
    except Exception as error:
        print(error)


@admin_required
def delete_schedule(request, id):

    service = ShedulesService()

    try:
        if request.method == "POST":
            service.delete_schedule(id)
            return redirect(reverse('list_schedule'))
        return redirect(reverse('list_schedule'))
    except Exception as error:
        print(str(error))
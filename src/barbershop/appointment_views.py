from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from barbershop.services import ServicePrice, ServiceAppointment, ShedulesService
from barbershop.validator import available_day
from barbershop.utils import day_week, generate_hours, free_hours, recover_name_week_day
from accounts.services import UserService
from django.contrib import messages
from django.urls import reverse
from accounts import exception
import traceback
from datetime import datetime
from django.utils.timezone import now


@login_required
def register_appointment(request):
    
    try:

        service_price = ServicePrice()
        service = service_price.get_list_service_name()

        if request.method == "POST":

            day = available_day(request)
            
            service_user = UserService()
            user = service_user.get_user(request.user.email)
            instance_service = service_price.get_instace_service_name(request.POST.get('type'))
           
            service_appointment = ServiceAppointment()
            service_appointment.create_new_appointment(user, instance_service, day)
            messages.success(request, "Agendamento criado com sucesso")
            return redirect('list_appointment')
        
        return render(request,'AppointmentTemplates/register_appointment.html', {'service_type': service})
    except exception.ValidationException as error:
        messages.error(request, f"{str(error)}")
    except Exception as error:
        messages.error(request, f"{str(error)}")
        traceback.print_exc()

    return render(request,'AppointmentTemplates/register_appointment.html', {'service_type': service})

@login_required
def list_appointment(request):
    
    try:
        
        date = request.GET.get('q')
        current_date = now().date()

        service_appointment = ServiceAppointment()
        appointment_today = service_appointment.get_appointment_today()
        
        current_date = now().strftime("%Y-%m-%d")

        if appointment_today is None:
            return redirect('register_appointment')

        if date:
            
            appointment_date = service_appointment.get_appointment_date(date)
            return render(request, 'AppointmentTemplates/list_appointment.html', {'appointments': appointment_date, 'current_date':current_date})
        print(appointment_today)
        return render(request, 'AppointmentTemplates/list_appointment.html', {'appointments': appointment_today, 'current_date':current_date})
        
    except Exception as error:
        print(str(error))
        
@login_required
def search_list_appointment(request):

    date = request.GET.get('q')
    service_appointment = ServiceAppointment()
    if date:
        appointment_date = service_appointment.get_appointment_date(date)
        print(appointment_date)
        return render(request, 'AppointmentTemplates/search_list_appointment.html', {'appointments': appointment_date})
    return redirect('list_appointment')

@login_required
def delete_appointment(request, id):

    try:
    
        service_appointment = ServiceAppointment()
        service_appointment.delete_appointment(id)
        messages.success(request, "Agendamento cancelado com sucesso")
        return redirect('list_appointment')
    
    except Exception as error:
        messages.error(request, "Erro ao cancelar o agendamento")
    return reverse(redirect('list_appointment'))

@login_required
def finish_appointment(request, id):

    try:
       
        service_appointment = ServiceAppointment()
        service_appointment.finish_appointment(id)
        messages.success(request, "Finalização realizada com sucesso")
        return redirect('list_appointment')
        
    except Exception as error:
        messages.error("Ocorreu algum erro ao finalizar o atendimento")
    return redirect('list_appointment')

def reschedule_appointment(request, id):
    
    try:
        service_price = ServicePrice()
        service = service_price.get_list_service_name()

        if request.method == "POST":

            day = available_day(request)

            instance_service = service_price.get_instace_service_name(request.POST.get('type'))

            service_appointment = ServiceAppointment()
            service_appointment.update_appointment(id, day, instance_service)
            messages.success(request, "Serviço Reagendado com sucesso")
            return redirect('list_appointment')
            
        return render(request, 'AppointmentTemplates/reschedule_appointment.html', {'service_type': service, 'id':id})
    except Exception as error:
        messages.error(request, "Ocorreu ao alterar a data")
    
    return redirect('list_appointment')

@login_required
def hours_list(request):

    try:    

        date = request.GET.get('date_time')
    
        today = recover_name_week_day(date)

        work_hours = ShedulesService.get_hours_by_day_name_week(today)
        period_hours = generate_hours(work_hours.start_time, work_hours.end_time, work_hours.launch_time)

        day_hours = ServiceAppointment.get_appointment_any_day(datetime.strptime(date, '%Y-%m-%d'))

        available_hours = free_hours(day_hours , period_hours)

        return render(request, 'AppointmentTemplates/hours_dropdown.html', {'available_hours': available_hours})
    
    except Exception as error:
        print(error)
    return redirect(reverse('register_appointment'))
    
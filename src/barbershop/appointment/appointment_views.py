import traceback
import pytz
from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from django.contrib import messages
from django.urls import reverse

from barbershop.appointment.service import ServiceAppointment
from barbershop.schedule.service import ShedulesService
from barbershop.service.service import ServicePrice
from barbershop.validator import available_day
from barbershop.query import BarbershopService
from barbershop.utils import day_week, generate_hours, free_hours, recover_name_week_day

from accounts.services import UserService
from accounts import exception


@login_required
def register_appointment(request):
    
    try:
        
        service = ServicePrice.get_list_service_name(request.user.id)
        clients = BarbershopService.get_client_by_email_barbeshop(request.user.id)
        
        schedule_service = ShedulesService()
        schedule = schedule_service.get_list_shedules(request.user)

        if request.method == "POST":

            client_id = request.POST.get('client')
            day = available_day(request, client_id)

            instance_service = ServicePrice.get_instace_service_name(request.POST.get('type'), request.user.id)
            ServiceAppointment.create_new_appointment(client_id, instance_service, day)
            messages.success(request, "Agendamento criado com sucesso")
            
            return redirect('list_appointment')
        
        if request.method == "GET":

            if not service:
                messages.warning(request, "Você deve cadastrar um serviço para abrir a página de agendamento")
                return redirect('register_service')
            
            if not schedule:
                messages.warning(request, "Você deve cadastrar um horários de atendimento para abrir a página de agendamento")
                return redirect('register_schedule')

            if not clients:
                messages.warning(request, "Você deve cadastrar um cliente para abrir a página de agendamento")
                return redirect('register_client')


            return render(request,'AppointmentTemplates/register_appointment.html', {'clients':clients, 'service_type': service})
    
    except exception.ValidationException as error:
        messages.error(request, f"{str(error)}")
    except Exception as error:
        messages.error(request, f"{str(error)}\ {traceback.print_exc()}")
        

    return render(request,'AppointmentTemplates/register_appointment.html', {'clients':clients, 'service_type': service})

@login_required
def list_appointment(request):
    
    try:
        
        date = request.GET.get('q')
        current_date = now().date()

        service_appointment = ServiceAppointment()
        appointment_today = service_appointment.get_appointment_today(request.user.id)
        timezone_sp = pytz.timezone("America/Sao_Paulo")
        current_date = datetime.now(timezone_sp).strftime("%Y-%m-%d")

        if appointment_today is None:
            return redirect('register_appointment')

        if date:
            
            appointment_date = service_appointment.get_appointment_date(date, request.user.id)
            return render(request, 'AppointmentTemplates/list_appointment.html', {'appointments': appointment_date, 'current_date':current_date})
        
        return render(request, 'AppointmentTemplates/list_appointment.html', {'appointments': appointment_today, 'current_date':current_date})
        
    except Exception as error:
        messages.error(request, f"{str(error)}\ {traceback.print_exc()}")
    
    return render(request, 'AppointmentTemplates/list_appointment.html', {'appointments': appointment_today, 'current_date':current_date})

@login_required
def search_list_appointment(request):

    date = request.GET.get('q')
    service_appointment = ServiceAppointment()
    if date:
        appointment_date = service_appointment.get_appointment_date(date)
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
        service = service_price.get_list_service_name(request.user)

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

        work_hours = ShedulesService.get_hours_by_day_name_week(today, request.user.id)
        period_hours = generate_hours(work_hours.start_time, work_hours.end_time, work_hours.launch_time)

        day_hours = ServiceAppointment.get_appointment_any_day(request.user.id, datetime.strptime(date, '%Y-%m-%d'))

        available_hours = free_hours(day_hours , period_hours)

        return render(request, 'AppointmentTemplates/hours_dropdown.html', {'available_hours': available_hours})
    
    except Exception as error:
        messages.error(request, str(error))
    return redirect(reverse('register_appointment'))
    
from datetime import datetime
from barbershop.utils import recover_name_week_day, generate_hours, free_hours
from barbershop.schedule.service import ShedulesService
from barbershop.appointment.service import ServiceAppointment
from chatbot.utils import conveter_data


def recover_hours(recive_message, admin_id):

    data_formatada = datetime.strptime(recive_message, "%d/%m/%Y").strftime("%Y-%m-%d")

    today = recover_name_week_day(data_formatada)

    work_hours_exists = ShedulesService.get_hours_by_day_name_week_exists(today, admin_id)
    
    if work_hours_exists:
        
        work_hours = ShedulesService.get_hours_by_day_name_week(today, admin_id)
        
        period_hours = generate_hours(work_hours.start_time, work_hours.end_time, work_hours.launch_time)

        day_hours = ServiceAppointment.get_appointment_any_day(admin_id, data_formatada)

        available_hours = free_hours(day_hours , period_hours)
    
        return True, available_hours
    return False, []

def exists_day_and_hour_available(day, hours, client_id):

    day_format = conveter_data(day)
    
    date_time_str = day_format + "T" + hours
 
    new_appointment_time = datetime.strptime(date_time_str, '%Y-%m-%dT%H:%M')
   
    service_appointment = ServiceAppointment()
    exits_datetime = service_appointment.get_hours_has_status_canceled(new_appointment_time, client_id)

    return True if not exits_datetime else False
                        
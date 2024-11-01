from barbershop.appointment.service import ServiceAppointment
from accounts.exception import ValidationException
from datetime import datetime, timedelta


def available_day(request):


    if request.POST.get('hours') == None:
        raise ValidationException(f"Não temos horários disponivel para este dia")
    print(request.POST.get('date_time'))
    print(request.POST.get('hours'))

    date_time_str = request.POST.get('date_time') + "T" + request.POST.get('hours')
    print(date_time_str)
    new_appointment_time = datetime.strptime(date_time_str, '%Y-%m-%dT%H:%M')
   
    service_appointment = ServiceAppointment()
    exits_datetime = service_appointment.get_hours_has_status_canceled(new_appointment_time)

    if exits_datetime:
        raise ValidationException(f"Horários indisponível {new_appointment_time}, agende outro horário")
    return new_appointment_time

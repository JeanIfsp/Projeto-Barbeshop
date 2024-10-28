from datetime import datetime
from barbershop.services import ShedulesService, ServiceAppointment
from barbershop.utils import recover_name_week_day, generate_hours, free_hours


def recover_hours(recive_message):

    data_formatada = data_formatada = datetime.strptime(recive_message, "%d/%m/%Y").strftime("%Y-%m-%d")
    today = recover_name_week_day(data_formatada)

    work_hours = ShedulesService.get_hours_by_day_name_week(today)
    period_hours = generate_hours(work_hours.start_time, work_hours.end_time, work_hours.launch_time)

    day_hours = ServiceAppointment.get_appointment_any_day(data_formatada)

    available_hours = free_hours(day_hours , period_hours)
    return available_hours

                        
from datetime import datetime, timedelta, date, time
import calendar

def day_week(data_str):

    data = datetime.strptime(data_str, '%Y-%m-%d')

    dias_da_semana = ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado", "Domingo"]

    return dias_da_semana[data.weekday()].upper()

def day_week_text(data):


    dias_da_semana = ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado", "Domingo"]

    return dias_da_semana[data.weekday()].upper()

def generate_hours(start_time, end_time, launch_time):

    current_time = datetime.combine(date.today(), start_time)
    end_time_dt = datetime.combine(date.today(), end_time)

    horarios = []
    
    while current_time.time() < end_time_dt.time():
        
        if current_time.time() == time(12, 0):  # Pular horário de almoço
            current_time += timedelta(hours=int(launch_time))
            continue
        
        horarios.append(current_time.strftime('%H'))
        current_time += timedelta(hours=1)
    
    return horarios

def free_hours(hours, scheduled_times):

    hours_str = []

    for hour in hours:
        
        if len(str(hour)) == 1:
            hours_str.append(f'0{str(hour)}')
            continue
        hours_str.append(str(hour))
    
    result = []

    for hour in scheduled_times:
        print(f'hour: {hour} hours_str: {hours_str}')
        if hour in hours_str:
            continue
        result.append(f'{hour}:00')
    
    return result

def get_month_name(month_number):

    meses = [
        "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
        "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
    ]

    return meses[month_number - 1]

def retrieve_month_names(distinct_months):
    
    months_with_names = [
        {'month_number': entry['month'], 'month_name': calendar.month_name[entry['month']].capitalize()}
        for entry in distinct_months
    ]

    return months_with_names

def converter_month_to_nuber(month_name):
    # Dicionário que mapeia os meses em português para seus números
    month = {
        "janeiro": 1,
        "fevereiro": 2,
        "março": 3,
        "abril": 4,
        "maio": 5,
        "junho": 6,
        "julho": 7,
        "agosto": 8,
        "setembro": 9,
        "outubro": 10,
        "novembro": 11,
        "dezembro": 12
    }
    
    # Retorna o número do mês ou None se o mês não for encontrado
    return month.get(month_name.lower())

def recover_name_week_day(date):
    day = day_week(date)
    return day.replace('Á', 'A') if 'Á' in day else day

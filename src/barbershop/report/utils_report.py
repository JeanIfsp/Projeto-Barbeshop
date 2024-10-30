from barbershop.utils import get_month_name
from datetime import datetime

def extract_month_count_data(data_by_month_and_type):

    months = []
    cuts_by_type = {}

    for entry in data_by_month_and_type:
        month_name = get_month_name(entry['month'])  # Função para traduzir mês
        if month_name not in months:
            months.append(month_name)
        
        service_type = entry['type_id__service_type']
        if service_type not in cuts_by_type:
            cuts_by_type[service_type] = []
        cuts_by_type[service_type].append(entry['total_cuts'])
    
    return  {
            'months': months,
            'cuts_by_type': cuts_by_type,
        }

def extract_week_count_data(data_by_week_and_type):

    days_weekend = {
    1: 'Domingo',
    2: 'Segunda-feira',
    3: 'Terça-feira',
    4: 'Quarta-feira',
    5: 'Quinta-feira',
    6: 'Sexta-feira',
    7: 'Sábado'
}


    day_week = []
    cuts_by_type = {}

    for entry in data_by_week_and_type:

        day_name = days_weekend[entry.get("weekday")]  # Nome do dia da semana
        day_month = entry.get("day_month").strftime("%d/%m/%y")  # Formatação da data
        day_name_more_month = f"{day_name}\n{day_month}"  # Combinação do nome do dia e da data
        
        day_week.append(day_name_more_month)  # Adiciona à lista de dias da semana
        
        service_type = entry['type_id__service_type']  # Tipo de serviço
        if service_type not in cuts_by_type:
            cuts_by_type[service_type] = []  # Inicializa a lista se o tipo de serviço não existir
        cuts_by_type[service_type].append(entry['total_cuts'])
    
    return {'months': day_week, 
    'cuts_by_type': cuts_by_type  
    }



def extract_month_amount_data(data_by_month_and_type):

    months = []
    cuts_by_type = {}

    
    for entry in data_by_month_and_type:
        month_name = get_month_name(entry['month'])  # Função para traduzir mês
        if month_name not in months:
            months.append(month_name)
        
        service_price = entry['type_id__service_type']  # Converte para float se for Decimal

        if service_price not in cuts_by_type:
            cuts_by_type[service_price] = []
        
        cuts_by_type[service_price].append(float(entry["total_price"]))

    return {
        'months': months,
        'cuts_by_type': cuts_by_type,
    }   
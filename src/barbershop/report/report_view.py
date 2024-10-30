import ast
from barbershop.permissions import admin_required
from django.shortcuts import render
from barbershop.appointment.service import ServiceAppointment
from barbershop.report.service import ServiceReport
from barbershop.service.service import ServicePrice
from barbershop.utils import  retrieve_month_names
from barbershop.report.utils_report import extract_month_count_data, extract_week_count_data, extract_month_amount_data
from django.http import JsonResponse
from django.utils import timezone

@admin_required
def report(request):

    try:
        service_price = ServicePrice()
        service = service_price.get_list_service_register()

        service_appointment = ServiceAppointment()
        months_saved_appointment = service_appointment.get_saved_month_appointment()
        months_name = retrieve_month_names(months_saved_appointment)
    
        return render(request, 'reportTemplates/report.html', {'services': list(service), 'months':months_name})
    
    except Exception as error:
        print(str(error))

@admin_required
def report_week(request):

    service_price = ServicePrice()
    service = service_price.get_list_service_register()
    return render(request, 'reportTemplates/report_week.html', {'services': list(service)})

@admin_required
def report_amount(request):

    service_price = ServicePrice()
    service = service_price.get_list_service_register()

    service_appointment = ServiceAppointment()
    months_saved_appointment = service_appointment.get_saved_month_appointment()
    months_name = retrieve_month_names(months_saved_appointment)

    return render(request, 'reportTemplates/report_amount.html', {'services': list(service), 'months':months_name})

def recover_data(request):

    
    mes = request.GET.get("mes")
    tipo_corte = request.GET.get("tipo_corte")

    service_report = ServiceReport()

    try:

        if mes == "Todos" and tipo_corte == "Todos":
            
            data_by_month_and_type = service_report.get_all_appointment()
            data = extract_month_count_data(data_by_month_and_type)

            return JsonResponse(data)
        
        elif mes == "Todos" and tipo_corte != "Todos": 
            tipo_corte_id = ast.literal_eval(tipo_corte).get("ID")
            data_by_month_and_type = service_report.get_data_by_type_id(tipo_corte_id)
            data = extract_month_count_data(data_by_month_and_type
                                            )
            return JsonResponse(data)
        
        elif mes != "Todos" and tipo_corte == "Todos":

            mes_dict = ast.literal_eval(mes)
            month_number = mes_dict.get('MONTH_NUMBER')

            data_by_month_and_type = service_report.get_data_by_month_number(month_number)
            data = extract_month_count_data(data_by_month_and_type)

            return JsonResponse(data)
        
        mes_dict = ast.literal_eval(mes)
        month_number = mes_dict.get('MONTH_NUMBER')

        tipo_corte_dict = ast.literal_eval(tipo_corte)
        type_id = tipo_corte_dict.get('ID')

        data_by_month_and_type = service_report.get_data_by_month_number_and_type_id(month_number, type_id)
        data = extract_month_count_data(data_by_month_and_type)

        return JsonResponse(data)
    
    except Exception as erro:
        return JsonResponse(erro)


def recover_data_week(request):
    
    try:

        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")
        tipo_corte = request.GET.get("tipo_corte")
    
        tipo_corte_id = ast.literal_eval(tipo_corte).get("ID")

        start_date_obj= timezone.datetime.strptime(start_date, "%Y-%m-%d")
        end_date_obj = timezone.datetime.strptime(end_date, "%Y-%m-%d")

        service_report = ServiceReport()
        data_by_week_and_type = service_report.get_data_by_week(start_date_obj, end_date_obj, tipo_corte_id)
        print(data_by_week_and_type)
        data = extract_week_count_data(data_by_week_and_type)

        return JsonResponse(data)
    
    except Exception as erro:
        return JsonResponse(erro)

def recover_data_amount(request):

    mes = request.GET.get("mes")
    tipo_corte = request.GET.get("tipo_corte")
    print(tipo_corte)
    service_report = ServiceReport()

    if mes == "Todos" and tipo_corte == "Todos":
            
        monthly_service_price_sum = service_report.get_all_amount()
        data = extract_month_amount_data(monthly_service_price_sum)
        return JsonResponse(data)
        
    elif mes == "Todos" and tipo_corte != "Todos": 
        tipo_corte_id = ast.literal_eval(tipo_corte).get("ID")
        data_by_month_and_type = service_report.get_data_by_type_id_amount(tipo_corte_id)
        data = extract_month_count_data(data_by_month_and_type
                                        )
        return JsonResponse(data)
    
    elif mes != "Todos" and tipo_corte == "Todos":
    
        mes_dict = ast.literal_eval(mes)
        month_number = mes_dict.get('MONTH_NUMBER')

        data_by_type_all_month = service_report.get_data_by_month_number_amount(month_number)
        data = extract_month_count_data(data_by_type_all_month)

        return JsonResponse(data)
    
    mes_dict = ast.literal_eval(mes)
    month_number = mes_dict.get('MONTH_NUMBER')

    tipo_corte_dict = ast.literal_eval(tipo_corte)
    type_id = tipo_corte_dict.get('ID')

    data_by_month_and_type = service_report.get_data_by_month_number_and_type_id_amount(month_number, type_id)
    data = extract_month_count_data(data_by_month_and_type)

    return JsonResponse(data)
   


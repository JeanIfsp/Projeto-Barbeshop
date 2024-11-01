import re

def validate_update_service_price(haircut_price):

    pattern = r"^\d+([.,]00)?$"
    if not re.match(pattern, haircut_price):
        raise ValueError("Por gentileza informe o valor neste padrão, por exemplo: 20.00")
    return True
    
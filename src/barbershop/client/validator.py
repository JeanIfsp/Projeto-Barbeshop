import re
from .service import ClientService
from .exception import ValidationException

def validator_client_name(client_name: str):

    if len(client_name) < 3:
        raise ValidationException("Para o nome do estabelecimento, necessita ter pelo menos 4 caracteres")
    return client_name

def validator_cell_phone_number(cell_phone_number: str):
    
    regex_cell_phone_number = r"^\d{11}$"
 
    if not bool(re.match(regex_cell_phone_number, cell_phone_number)):
        raise ValidationException("Informe o número com a quantidade de caracter igual a do exemplo")
    elif ClientService.get_client_cell_phone_number_exists(cell_phone_number):
        raise ValidationException("O Celular Informado já está cadastrado")
    return cell_phone_number

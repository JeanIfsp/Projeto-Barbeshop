import re
from accounts.exception import ValidationException
from accounts.services import UserService


def validator_barbeshop_name(barbershop_name: str):

    if len(barbershop_name) < 3:
        raise ValidationException("Para o nome do estabelecimento, necessita ter pelo menos 4 caracteres")
    return barbershop_name


def validator_email(email: str):

    email_regex = r"^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    
    if not re.match(email_regex, email):
        raise ValidationException("O e-mail não está em um formato válido")
    return email


def validator_password(password: str):

    if not re.search(r"[A-Z]", password):
        raise ValidationException("A senha precisa ter pelo menos uma letra maiúscula.")

    if not re.search(r"[a-z]", password):
        raise ValidationException("A senha precisa ter pelo menos uma letra minúscula.")

    if not re.search(r"\d", password):
        raise ValidationException("A senha deve ter pelo menos um número.")

    if not re.search(r"[!@#$%^&*(),.?:{}|<>]", password):
        raise ValidationException("A senha deve ter pelo menos caractere especial.")

    if len(password) < 8:
        raise ValidationException("A senha dever ter pelo menos 8 caracteres.")

    return password

def validator_cell_phone_number(cell_phone_number: str):
    
    regex_cell_phone_number = r"^\d{11}$"
 

    if not bool(re.match(regex_cell_phone_number, cell_phone_number)):
        raise ValidationException("Informe o número com a quantidade de caracter igual a do exemplo")
    elif UserService.get_user_cell_phone_number(cell_phone_number):
        raise ValidationException("O Celular Informado já está cadastrado")
    return cell_phone_number

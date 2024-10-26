import re
from accounts.exception import ValidationException


def validator_username(username: str):

    if len(username) < 3:
        raise ValidationException("Username precisa ter pelo menos 4 caracteres")
    return username


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

def validator_age(age: str):
    
    age_info = int(age)

    if age_info < 1:
        raise ValidationException("Idate Errada.")
    
    return age_info
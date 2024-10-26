from itsdangerous import URLSafeTimedSerializer
from django.conf import settings
from datetime import datetime, timedelta

def generate_password_reset_token(token):

    serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
    
    return serializer.dumps(token, salt=settings.SECRET_KEY)

def verify_password_reset_token(token, expiration=300):  # 300 segundos = 5 minutos

    serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
    
    try:
        email = serializer.loads(token, salt=settings.SECRET_KEY, max_age=expiration)
    except:
        return None
    return email

def verify_date_token(token, expiration=300):  # 300 segundos = 5 minutos
    """
        Verifica se a data no token é válida e não passou mais de 5 minutos.
    """
    serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
    
    try:

        date_str = serializer.loads(token, salt=settings.SECRET_KEY, max_age=expiration)
        
        token_date = datetime.strptime(date_str, '%d/%m/%Y %H:%M')
        
        now = datetime.now()
        
        if now - token_date > timedelta(minutes=5):
            return False  
        
        return True  
    
    except Exception as e:
        return False  
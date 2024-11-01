import re

def value_is_number(recive_message):
    
    pattern = "^(1?[0-9]|20)$" 
    
    return  bool(re.match(pattern, recive_message))

def conveter_data(date):

    from datetime import datetime

    data_obj = datetime.strptime(date, "%d/%m/%Y")

    return data_obj.strftime("%Y-%m-%d")

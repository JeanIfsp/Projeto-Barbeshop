import re

def value_is_number(recive_message):
    
    pattern = "^(1?[0-9]|20)$" 
    
    return  bool(re.match(pattern, recive_message))

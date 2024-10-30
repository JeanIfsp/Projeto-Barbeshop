
MESSAGES_INITIALIZE = """
    *Olá %s, Seja Bem-Vindo à Barbeshop!*

    _Lembramos que este contato é para solicitação_  
    _de agendamento de nossos serviços._

    *Como podemos ajudá-lo?* 😊

    Digite o número correspondente à sua escolha:

    *%s* - Já sou cliente  
    *%s* - Quero me cadastrar
"""

MESSAGES_CLIENT_EXISTS = """
    %s Deseja Agendar seu atendimento:
*1 - Sim* 
*2 - Não*
"""

MESSAGE_INFORMATION_CLIENTE_FORMATE_DATA = """
    %s por gentileza, informe o dia desejado para agendar seu atendimento no seguinte formato: \n %s
"""

MESSAGE_CHOOSE_YOUR_APPOINTMENT_TIME = """
    %s temos esses horários disponíveis para agendamento:
    %s hs
"""

MESSAGE_CHOOSE_YOUR_SERVICE_TYPE = """
    %s temos esses serviços disponíveis para agendamento:
    %s
"""


MESSAGES_INFORMATION_REGISTER_APPOINTMENT = """
    %s confirma o seu agendamento para ás: *%s hs* no dia *%s* serviço de *%s*\n
*1 - Sim* 
*2 - Não*
"""

MESSAGE_FINISH_REFISTER_APPOINTMENT = """
*%s Muito obrigado por agendar seu horário conosco!*
*Até breve ✂️😊*
*Estamos até aguardando.*
"""

MESSAGES = {
    "InitializeBotOptions": MESSAGES_INITIALIZE,
    "OptionsClient": {
        "0":MESSAGES_CLIENT_EXISTS,
        "1":MESSAGE_INFORMATION_CLIENTE_FORMATE_DATA,
        "2":MESSAGE_CHOOSE_YOUR_APPOINTMENT_TIME,
        "3":MESSAGE_CHOOSE_YOUR_SERVICE_TYPE,
        "4":MESSAGES_INFORMATION_REGISTER_APPOINTMENT,
        "5":MESSAGE_FINISH_REFISTER_APPOINTMENT
        }


                            
}


def recover_message(key, *args):
    print('args: ', args)    
    message = MESSAGES.get(key)
    message_add_values = message % args
    print(message_add_values)
    return message_add_values

def recover_messar_with_action(key, action, *args):
    print("key: ", key)
    print("action: ", action)
    print("Args: ", args)
    message = MESSAGES[key][str(action)]
    message_add_values = message % args
    print("message_add_values: ", message_add_values)
    return message_add_values

def create_message_to_show_service(service_name):

    result =  "\n".join([f"{i} - {service}" for i, service in enumerate(service_name)])
    print(result)
    return result
       
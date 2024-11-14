
MESSAGES_INITIALIZE = """
    *Olá %s, Seja Bem-Vindo à Barbeshop!*

    _Lembramos que este contato é para solicitação_  
    _de agendamento de nossos serviços._

    *Como podemos ajudá-lo?* 😊
    
    *Deseja se cadastrar ?*
    
    Digite o número correspondente à sua escolha:

    *1 - Sim* 
    *2 - Não*
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
    %s confirma o seu agendamento para ás: *%s hs* no dia *%s* serviço de *%s* *%s*\n
    *%s*\n
*1 - Sim* 
*2 - Não*
"""

MESSAGE_FINISH_REFISTER_APPOINTMENT = """
*%s Muito obrigado por agendar seu horário conosco!*
*Até breve ✂️😊*
*Estamos até aguardando.*
"""

MESSAGE_QUESTION_REGISTER_USER = """
📲 *%s* podemos salvar os seguintes dados:\n
*Nome:* %s
*what's up:* %s\n

*1 - Sim*
*2 - Não*
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
        },
    "RegisterUser":{
        "1":MESSAGE_QUESTION_REGISTER_USER
    }


                            
}


def recover_message(key, *args):
  
    message = MESSAGES.get(key)
    message_add_values = message % args
    return message_add_values

def recover_messar_with_action(key, action, *args):

    message = MESSAGES[key][str(action)]
    message_add_values = message % args
    return message_add_values


def create_message_to_show_hours(hours):

    result = "\n".join([f"{i} - {hour}" for i, hour in enumerate(hours)])
    return result

def create_message_to_show_service(service_name):

    result =  "\n".join([f"{i} - {service}" for i, service in enumerate(service_name)])
    return result
       

def create_message_to_show_name_and_place_barbeshop(barbershops):

    message = "📋 *Lista de Barbearias Disponíveis:*\n\n"
    for i, barber in enumerate(barbershops):
        message += f" *{i}* - ✂️ *{barber.name_barbershop}*\n   📍 Endereço: {barber.address}\n\n"
    message += "*Informe por gentileza o número do estabelecimento que deseja agendar o serviço*"
    return message

MESSAGES_INITIALIZE = """
*Olá %s, Seja Bem-Vindo à Barbeshop!*

_Lembramos que este contato é para solicitação_  
_de agendamento de nossos serviços._

*Como podemos ajudá-lo?* 😊

Digite o número correspondente à sua escolha:

*%s* - Já sou cliente  
*%s* - Quero me cadastrar
"""

MESSAGES = {
    "InitializeBotOptions": MESSAGES_INITIALIZE


                            
}


def recover_message(key, *args):
    print('args: ', args)
    message = MESSAGES.get(key)
    message_add_values = message % args
    return message_add_values



import os
from twilio.rest import Client
from rest_framework.decorators import api_view
from django.http import HttpResponse
from twilio.twiml.messaging_response import MessagingResponse


from .dispatch import Orquestrador

@api_view(['GET','POST'])
def bot_message(request):
    
    if request.method == 'GET':
        return HttpResponse("Dia Lindo")


   

    session_exists = False

    if not session_exists:
        print("request: ", request.POST.dict())

        orquestrador = Orquestrador(request)
        message_receive = request.POST.get("Body")
        print("profile: ", request.POST.dict().get("ProfileName"))
        send_message = orquestrador.reply(message_receive)
        response = MessagingResponse()
        response.message(send_message)
        return HttpResponse(str(response), content_type='application/xml')
    # is cliente

    if True:

       a = {"intent":AgendarBotClient.AGENDAR_HOJE, "action": IsClientBotOptions.AGENDAR}
        
    return HttpResponse(str(response), content_type='application/xml')
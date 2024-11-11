
import os
from twilio.rest import Client
from rest_framework.decorators import api_view
from django.http import HttpResponse
from twilio.twiml.messaging_response import MessagingResponse


from .dispatch import Orquestrador

@api_view(['POST'])
def bot_message(request):
    print(request.data)
    orquestrador = Orquestrador(request)
    message_receive = request.POST.get("Body")
    send_message = orquestrador.reply(message_receive)
    response = MessagingResponse()
    response.message(send_message)
    return HttpResponse(str(response), content_type='application/xml')

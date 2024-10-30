import re
from datetime import datetime
from .cache import RedisManager
from .message import recover_message, recover_messar_with_action, create_message_to_show_service
from .controller import recover_hours
from accounts.services import UserService
from barbershop.service.service import ServicePrice
from barbershop.utils import day_week, generate_hours, free_hours, recover_name_week_day
from barbershop.appointment.service import ServiceAppointment 
from barbershop.schedule.service import  ShedulesService


class InitializeBotOptions:

    INITIALIZER = 0
    IS_CLIENT = 1
    IS_REGISTER = 2

class OptionsClient:

    INITIALIZE_QUESTION = 0
    INFORMATION_FORMAT_DATA = 1
    CHOOSE_YOUR_APPOINTMENT_TIME = 2
    CHOOSE_YOUR_SERVICE_TYPE = 3
    REGISTER_APPOINTMENT = 4
    FINISH_REGISTER_APPOINTMENT = 5


class Orquestrador:


    def __init__(self, request) -> None:
        self.profile_name = request.POST.get("ProfileName")
        self.cell_phone_number_client = request.POST.get("From").replace("whatsapp:+55", "")
        self.redis = RedisManager()

    def crate_context(self, intent, action, data):
        self.redis.set_key(self.cell_phone_number_client, {"intent":intent, "action":action, "data":data})
         

    def reply(self, recive_message):


        user_exists = UserService.get_user_cell_phone_number(self.cell_phone_number_client)
        session_exists = self.redis.get_key(self.cell_phone_number_client)
        
        if not session_exists and user_exists:

            self.crate_context(InitializeBotOptions.IS_CLIENT,  OptionsClient.INITIALIZE_QUESTION, None)
            return recover_messar_with_action("OptionsClient",
                                   OptionsClient.INITIALIZE_QUESTION,
                                   self.profile_name)
        
        current_date = datetime.now().strftime("%d/%m/%Y")

        if not self.redis.get_key(self.cell_phone_number_client):

            self.crate_context(0, 0, None)
            return recover_message("InitializeBotOptions",
                                self.profile_name,
                                InitializeBotOptions.IS_CLIENT,
                                InitializeBotOptions.IS_REGISTER
                                )
            
        print("session_exists: ", session_exists)
        if self.redis.get_key(self.cell_phone_number_client).get('intent') == 1:
            
            if self.redis.get_key(self.cell_phone_number_client).get('action') == 0:
            
                if recive_message == "1":

                    current_date = datetime.now().strftime("%d/%m/%Y")
                    self.crate_context(InitializeBotOptions.IS_CLIENT, OptionsClient.INFORMATION_FORMAT_DATA, None)
                    return recover_messar_with_action("OptionsClient",
                                           OptionsClient.INFORMATION_FORMAT_DATA,
                                           self.profile_name,
                                           current_date
                                           )
              
            
            elif self.redis.get_key(self.cell_phone_number_client).get('action') == 1:

                pattern = r'^(0?[1-9]|[12][0-9]|3[01])/(0?[1-9]|1[0-2])/[0-9]{4}$'

                if re.match(pattern, recive_message):
                 
                    if datetime.strptime(recive_message, "%d/%m/%Y") >= datetime.now():
               
                        available_hours = recover_hours(recive_message)

                        available_hours_format = "hs \n ".join(available_hours)
                        
                        self.crate_context(InitializeBotOptions.IS_CLIENT, OptionsClient.CHOOSE_YOUR_APPOINTMENT_TIME, recive_message)
                        
                        return recover_messar_with_action("OptionsClient",
                                                   OptionsClient.INFORMATION_FORMAT_DATA,
                                                   self.profile_name,
                                                   available_hours_format)
                    
                    return recover_messar_with_action("OptionsClient",
                                           OptionsClient.INFORMATION_FORMAT_DATA,
                                           self.profile_name,
                                           current_date
                                           )
                
                return f"A data que você informou não segue o padrão, Por gentileza informe este pasd~soe de data commo exemplo: {current_date}"
            
            elif self.redis.get_key(self.cell_phone_number_client).get('action') == 2:

                pattern = r'^(?:([01]?\d|2[0-3]):([0-5]\d)|([01]?\d|2[0-3])) ?(?:hs)?$'

                if re.match(pattern, recive_message):

                    service_type = ServicePrice.get_list_service_name()
                    list_service_type = "\n".join(list(service_type))

                    data = {}
                    data["day"] = self.redis.get_key(self.cell_phone_number_client).get('data')
                    data["hours"] = recive_message
                    data["sevice_type"] = list(service_type)
                
                    self.crate_context(InitializeBotOptions.IS_CLIENT, OptionsClient.CHOOSE_YOUR_SERVICE_TYPE, data)
                    
                    return recover_messar_with_action("OptionsClient",
                                                      OptionsClient.CHOOSE_YOUR_SERVICE_TYPE,
                                                      self.profile_name,
                                                      create_message_to_show_service(list(service_type))
                                                      )
                recive_message = self.redis.get_key(self.cell_phone_number_client).get("data")
                available_hours = recover_hours(recive_message)
                available_hours_format = "hs \n ".join(available_hours)
                        
                return recover_messar_with_action("OptionsClient",
                                                   OptionsClient.INFORMATION_FORMAT_DATA,
                                                   self.profile_name,
                                                   available_hours_format) 
            
            elif self.redis.get_key(self.cell_phone_number_client).get('action') == 3:

                data = self.redis.get_key(self.cell_phone_number_client).get('data')
                service_type = data.get("sevice_type")

                pattern = "^(1?[0-9]|20)$" 

                if bool(re.match(pattern, recive_message)):

                    type_service = service_type[int(recive_message)]
                    print("type_service: ", type_service)
                    data_user = {"day": data.get("day"), "hours": data.get("hours"),"service_type": type_service}
                    self.crate_context(InitializeBotOptions.IS_CLIENT,  OptionsClient.REGISTER_APPOINTMENT, data_user)
                    
                    return recover_messar_with_action("OptionsClient",
                                                      OptionsClient.REGISTER_APPOINTMENT,
                                                      self.profile_name,
                                                      data.get("hours"),
                                                      data.get("day"),
                                                      type_service
                                                      )
                
                return recover_messar_with_action("OptionsClient",
                                                      OptionsClient.CHOOSE_YOUR_SERVICE_TYPE,
                                                      self.profile_name,
                                                      create_message_to_show_service(list(service_type))
                                                      )
            elif self.redis.get_key(self.cell_phone_number_client).get('action') == 4:

                if recive_message == "1":
                    # TODO salvar agendamento

                    user = UserService.get_user_cell_phone_number(self.cell_phone_number_client)

                    self.redis.delete_key(self.cell_phone_number_client)
                    return recover_messar_with_action("OptionsClient",
                                                      OptionsClient.FINISH_REGISTER_APPOINTMENT,
                                                      self.profile_name,
                                                      )
                elif recive_message == "2":
                    self.crate_context(InitializeBotOptions.IS_CLIENT,  OptionsClient.INITIALIZE_QUESTION, None)
                else:
                    data = self.redis.get_key(self.cell_phone_number_client).get('data')
                    return recover_messar_with_action("OptionsClient",
                                                      OptionsClient.REGISTER_APPOINTMENT,
                                                      self.profile_name,
                                                      data.get("hours"),
                                                      data.get("day"),
                                                      data.get("service_type")
                                                      )
                
            
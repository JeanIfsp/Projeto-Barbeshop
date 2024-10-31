import re
from datetime import datetime
from .cache import RedisManager
from .message import recover_message, recover_messar_with_action, create_message_to_show_service
from .controller import recover_hours
from accounts.services import UserService
from accounts.validator import validator_first_name
from barbershop.service.service import ServicePrice
from barbershop.utils import day_week, generate_hours, free_hours, recover_name_week_day
from barbershop.appointment.service import ServiceAppointment 
from barbershop.schedule.service import  ShedulesService
from chatbot.utils import value_is_number


class InitializeBotOptions:

    INITIALIZER = 0
    IS_CLIENT = 1
    REGISTER_USER = 2

class OptionsClient:

    INITIALIZE_QUESTION = 0
    INFORMATION_FORMAT_DATA = 1
    CHOOSE_YOUR_APPOINTMENT_TIME = 2
    CHOOSE_YOUR_SERVICE_TYPE = 3
    REGISTER_APPOINTMENT = 4
    FINISH_REGISTER_APPOINTMENT = 5


class RegisterUser:

    QUESTION_NAME = 0
    FINISH_REGISTER_USER = 1
    COMPLETE = 2

class AnswerDefault:

    YES = "1"
    NO = "2"


class Orquestrador:


    def __init__(self, request) -> None:
        self.profile_name = request.POST.get("ProfileName")
        self.cell_phone_number_client = request.POST.get("From").replace("whatsapp:+55", "")
        self.redis = RedisManager()

    def crate_context(self, intent, action, data):
        self.redis.set_key(self.cell_phone_number_client, {"intent":intent, "action":action, "data":data})
         

    def reply(self, recive_message):


        session_exists = self.redis.get_key(self.cell_phone_number_client)
        
        if not session_exists:
            
            user_exists = UserService.get_user_cell_phone_number(self.cell_phone_number_client)
            
            if user_exists:

                self.crate_context(InitializeBotOptions.IS_CLIENT,  OptionsClient.INITIALIZE_QUESTION, None)
                return recover_messar_with_action("OptionsClient",
                                    OptionsClient.INITIALIZE_QUESTION,
                                    self.profile_name)
            else:

                self.crate_context(InitializeBotOptions.REGISTER_USER, RegisterUser.QUESTION_NAME, None)
                return recover_message("InitializeBotOptions",
                                    self.profile_name,
                                    )
        else:

            if self.redis.get_key(self.cell_phone_number_client).get('intent') == InitializeBotOptions.IS_CLIENT:
                
                return self.cliente(recive_message)
            
            return self.register_client(recive_message)
        
    def cliente(self, recive_message):

                
        current_date = datetime.now().strftime("%d/%m/%Y")
        
        if self.redis.get_key(self.cell_phone_number_client).get('action') == 0:
        
            if recive_message == AnswerDefault.YES:

                current_date = datetime.now().strftime("%d/%m/%Y")
                self.crate_context(InitializeBotOptions.IS_CLIENT, OptionsClient.INFORMATION_FORMAT_DATA, None)
                return recover_messar_with_action("OptionsClient",
                                        OptionsClient.INFORMATION_FORMAT_DATA,
                                        self.profile_name,
                                        current_date
                                        )
            
            elif recive_message == AnswerDefault.NO:

                return "🙏 Agradecemos pelo seu contato! Sempre que desejar agendar nossos serviços, estaremos à disposição para atendê-lo."
        
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
            
            return f"A data que você informou não segue o padrão, Por gentileza informe este padrões data commo exemplo: {current_date}"
        
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

            if value_is_number(recive_message):

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

    def register_client(self, recive_message): 

        if self.redis.get_key(self.cell_phone_number_client).get('intent') == 2:
            

            if self.redis.get_key(self.cell_phone_number_client).get('action') == 0:
                
                if value_is_number(recive_message):
                    
                    if recive_message == "1":
                        self.crate_context(InitializeBotOptions.REGISTER_USER, RegisterUser.FINISH_REGISTER_USER, None)
                        return "Por gentileza, informe como você gostaria de ser chamado ?"
                   
                    elif recive_message == "2":
                        self.redis.delete_key(self.cell_phone_number_client)
                        return "🙏 Agradecemos pelo seu contato! Sempre que desejar agendar nossos serviços, estaremos à disposição para atendê-lo."
            
                        
                return recover_message("InitializeBotOptions",
                                self.profile_name,
                                )

            
            if self.redis.get_key(self.cell_phone_number_client).get('action') == 1:
                
                if len(recive_message) > 3:
                    data = {"name": recive_message, "cell_phone_number": self.cell_phone_number_client}
                    self.crate_context(InitializeBotOptions.REGISTER_USER, RegisterUser.COMPLETE, data)


                    return recover_messar_with_action("RegisterUser",
                                        RegisterUser.FINISH_REGISTER_USER,
                                        recive_message,
                                        recive_message,
                                        self.cell_phone_number_client
                                        )
                
                return "Por gentileza, informe como você gostaria de ser chamado ?"
            

            if value_is_number(recive_message):
                
                if recive_message == AnswerDefault.YES:
                    data = self.redis.get_key(self.cell_phone_number_client).get("data")
                    UserService.create_client({"name":data.get("name"), "cell_phone_number": data.get("cell_phone_number")})
                    self.crate_context(InitializeBotOptions.IS_CLIENT,  OptionsClient.INITIALIZE_QUESTION, None)
                    return "✅ Cadastro realizado com sucesso!"
                
                elif recive_message == AnswerDefault.NO:
                    self.redis.delete_key(self.cell_phone_number_client)
                    return "🙏 Agradecemos pelo seu contato! Sempre que desejar agendar nossos serviços, estaremos à disposição para atendê-lo."
            
            data = self.redis.get_key(self.cell_phone_number_client).get("data")

            return recover_messar_with_action("RegisterUser",
                                        RegisterUser.FINISH_REGISTER_USER,
                                        data.get("name"),
                                        data.get("name"),
                                        data.get("cell_phone_number")
                                        )

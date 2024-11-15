import re
import json
from datetime import datetime
from django.core.serializers import serialize, deserialize
from chatbot.cache import RedisManager
from chatbot.controller import recover_hours, exists_day_and_hour_available
from accounts.services import UserService
from accounts.validator import validator_barbeshop_name
from barbershop.service.service import ServicePrice
from barbershop.utils import day_week, generate_hours, free_hours, recover_name_week_day
from barbershop.appointment.service import ServiceAppointment 
from barbershop.schedule.service import  ShedulesService
from barbershop.query import BarbershopService
from barbershop.client.service import ClientService
from chatbot.utils import value_is_number, conveter_data
from chatbot.message import (
    recover_message,
    recover_messar_with_action,
    create_message_to_show_service,
    create_message_to_show_hours,
    create_message_to_show_name_and_place_barbeshop
    )


class InitializeBotOptions:

    INITIALIZER = 0
    IS_CLIENT = 1
    REGISTER_USER = 2

class OptionsClient:

    INITIALIZE_QUESTION = 0
    INFORMATION_BARBERSHOP_ADDRES = 6
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

    @property
    def profile_name(self):
        return self._profile_name

    #
    @profile_name.setter
    def profile_name(self, profile_name):
        self._profile_name = profile_name
       

    def crate_context(self, intent, action, data, data_json):
        self.redis.set_key(self.cell_phone_number_client, {"intent":intent, "action":action, "data":data, "data_json":data_json})

    def reply(self, recive_message):


        session_exists = self.redis.get_key(self.cell_phone_number_client)
        
        if not session_exists:
            
            client_exists = ClientService.get_client_cell_phone_number(self.cell_phone_number_client)
            
            if client_exists:

                self.profile_name = client_exists.client_name 
                data = {"client_name": client_exists.client_name, "cliente_id": client_exists.id}
                self.crate_context(InitializeBotOptions.IS_CLIENT,  OptionsClient.INITIALIZE_QUESTION, data, None)
                return recover_messar_with_action("OptionsClient",
                                    OptionsClient.INITIALIZE_QUESTION,
                                    self.profile_name)
            else:

                self.crate_context(InitializeBotOptions.REGISTER_USER, RegisterUser.QUESTION_NAME, None, None)
                return recover_message("InitializeBotOptions",
                                    self.profile_name,
                                    )
        else:

            if self.redis.get_key(self.cell_phone_number_client).get('intent') == InitializeBotOptions.IS_CLIENT:
                
                return self.cliente(recive_message)
            
            return self.register_client(recive_message)
        
    def cliente(self, recive_message):

        current_date = datetime.now().strftime("%d/%m/%Y")
        
        if self.redis.get_key(self.cell_phone_number_client).get('action') == OptionsClient.INITIALIZE_QUESTION:
        
            if recive_message == AnswerDefault.YES:

                data_save_redis = self.redis.get_key(self.cell_phone_number_client).get('data')

                queryset_barbershops = BarbershopService.get_data_barbershop()
                data_json = serialize('json', queryset_barbershops)
                
                if queryset_barbershops:
                    self.crate_context(InitializeBotOptions.IS_CLIENT, OptionsClient.INFORMATION_BARBERSHOP_ADDRES, data_save_redis, data_json)
                    return create_message_to_show_name_and_place_barbeshop(queryset_barbershops)
                
                return "Não temos nenhuma barbearia cadastrada, entra em contato mais tarde conosco"
            
            elif recive_message == AnswerDefault.NO:

                self.redis.delete_key(self.cell_phone_number_client)
                return "🙏 Agradecemos pelo seu contato! Sempre que desejar agendar nossos serviços, estaremos à disposição para atendê-lo."

            return "Informe por gentileza uas da opções\n*1* - *SIM*\n*2* - *NÃO*"

        elif self.redis.get_key(self.cell_phone_number_client).get('action') == OptionsClient.INFORMATION_BARBERSHOP_ADDRES:
            
            data_save_redis = self.redis.get_key(self.cell_phone_number_client).get('data')
            self.profile_name = data_save_redis.get("client_name")
            data_json = self.redis.get_key(self.cell_phone_number_client).get("data_json")

            data_deserialize = deserialize('json', data_json)
            chosen_establishment = [obj.object for obj in data_deserialize]

            if value_is_number(recive_message):

                current_date = datetime.now().strftime("%d/%m/%Y")
                admin_id = chosen_establishment[int(recive_message)].admin.id
                barbershop_info = chosen_establishment[int(recive_message)]

                data_save_redis = self.redis.get_key(self.cell_phone_number_client).get('data')
   
                data_save_redis["admin_id"] = admin_id
                data_save_redis["barbershop_name"] = barbershop_info.name_barbershop
                data_save_redis["barbershop_address"] = barbershop_info.address

                self.crate_context(InitializeBotOptions.IS_CLIENT, OptionsClient.INFORMATION_FORMAT_DATA, data_save_redis, None)
                
                return recover_messar_with_action("OptionsClient",
                                        OptionsClient.INFORMATION_FORMAT_DATA,
                                        self.profile_name,
                                        current_date
                                        )

            return create_message_to_show_name_and_place_barbeshop(chosen_establishment)

        elif self.redis.get_key(self.cell_phone_number_client).get('action') == OptionsClient.INFORMATION_FORMAT_DATA:

            pattern = r'^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/([0-9]{4})$'

            if re.match(pattern, recive_message):

                if datetime.strptime(recive_message, "%d/%m/%Y").date() >= datetime.now().date():

                    data_save_redis = self.redis.get_key(self.cell_phone_number_client).get('data')
                    self.profile_name = data_save_redis.get("client_name")
                    admin_id = data_save_redis.get("admin_id")
                    work_hours_exists, available_hours = recover_hours(recive_message, admin_id)
                    
                    if work_hours_exists:

                        available_hours_format = create_message_to_show_hours(available_hours)
                        
                        data_save_redis["day"] = recive_message
                        data_save_redis["available_hours"] = available_hours
                        
                        self.crate_context(InitializeBotOptions.IS_CLIENT, OptionsClient.CHOOSE_YOUR_APPOINTMENT_TIME, data_save_redis, None)
                        
                        return recover_messar_with_action("OptionsClient",
                                                    OptionsClient.INFORMATION_FORMAT_DATA,
                                                    self.profile_name,
                                                    available_hours_format)
                    message = f"Não há horário cadastrado para este dia: {recive_message}, informe outro, por gentileza"
                    self.replay_exeception(message)
              
                
                return recover_messar_with_action("OptionsClient",
                                        OptionsClient.INFORMATION_FORMAT_DATA,
                                        self.profile_name,
                                        current_date
                                        )
            
            return f"A data que você informou não segue o padrão, Por gentileza informe este padrões data commo exemplo: {current_date}"
        
        elif self.redis.get_key(self.cell_phone_number_client).get('action') == OptionsClient.CHOOSE_YOUR_APPOINTMENT_TIME:

            data_save_redis = self.redis.get_key(self.cell_phone_number_client).get('data')

            self.profile_name = data_save_redis.get("client_name")

            if value_is_number(recive_message):

                admin_id = data_save_redis.get("admin_id")
                service_type = ServicePrice.get_list_service_name(admin_id)
                hour = data_save_redis.get("available_hours")

                data_save_redis["hours"] = hour[int(recive_message)]
                data_save_redis["sevice_type"] = list(service_type)
            
                self.crate_context(InitializeBotOptions.IS_CLIENT, OptionsClient.CHOOSE_YOUR_SERVICE_TYPE, data_save_redis, None)
                
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
        
        elif self.redis.get_key(self.cell_phone_number_client).get('action') == OptionsClient.CHOOSE_YOUR_SERVICE_TYPE:

            data = self.redis.get_key(self.cell_phone_number_client).get('data')
            service_type = data.get("sevice_type")
            self.profile_name = data.get("client_name")

            pattern = "^(1?[0-9]|20)$" 

            if value_is_number(recive_message):

                type_service = service_type[int(recive_message)]

                data_appointment = {"client_name":data.get("client_name"), "client_id": data.get("cliente_id"), "admin_id":data.get("admin_id"), "day": data.get("day"), "hours": data.get("hours"), "service_type": type_service}
                self.crate_context(InitializeBotOptions.IS_CLIENT,  OptionsClient.REGISTER_APPOINTMENT, data_appointment, None)
                
                return recover_messar_with_action("OptionsClient",
                                                    OptionsClient.REGISTER_APPOINTMENT,
                                                    self.profile_name,
                                                    data.get("hours"),
                                                    data.get("day"),
                                                    type_service,
                                                    data.get("barbershop_name"),
                                                    data.get("barbershop_address")
                                                    )
            
            return recover_messar_with_action("OptionsClient",
                                                    OptionsClient.CHOOSE_YOUR_SERVICE_TYPE,
                                                    self.profile_name,
                                                    create_message_to_show_service(list(service_type))
                                                    )
        
        elif self.redis.get_key(self.cell_phone_number_client).get('action') == OptionsClient.REGISTER_APPOINTMENT:

            data_appointment = self.redis.get_key(self.cell_phone_number_client).get("data")
            self.profile_name = data_appointment.get("client_name") 

            if recive_message == AnswerDefault.YES:
    
           
                if exists_day_and_hour_available(data_appointment.get("day"), data_appointment.get("hours"), data_appointment.get("client_id")):

                    client_exists = ClientService.get_client_cell_phone_number(self.cell_phone_number_client)
               
                    instance_service = ServicePrice.get_instace_service_name(data_appointment.get("service_type"), data_appointment.get("admin_id"))
                    
                    day_time = conveter_data(data_appointment.get("day")) + 'T' + data_appointment.get("hours")
                    date_time = datetime.strptime(day_time, '%Y-%m-%dT%H:%M')
                    
                    admin_id = data_appointment.get("admin_id")
                    client_id = data_appointment.get("client_id")
                    
                    if not ClientService.get_relationship_between_cliente_and_barbershop_pass_id(admin_id, client_id):

                        ClientService.create_relationship_between_cliente_and_barbershop_pass_id(admin_id, client_id)

                    ServiceAppointment.create_new_appointment(client_exists.id, instance_service, date_time)

                    self.redis.delete_key(self.cell_phone_number_client)
                    return recover_messar_with_action("OptionsClient",
                                                        OptionsClient.FINISH_REGISTER_APPOINTMENT,
                                                        self.profile_name,
                                                        )
                
                return recover_messar_with_action("OptionsClient",
                                    OptionsClient.INITIALIZE_QUESTION,
                                    self.profile_name)
            
            elif recive_message == AnswerDefault.NO:

                self.delete_key(self.cell_phone_number_client)
                return "🙏 Agradecemos pelo seu contato! Sempre que desejar agendar nossos serviços, estaremos à disposição para atendê-lo."
             
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

        if self.redis.get_key(self.cell_phone_number_client).get('intent') == InitializeBotOptions.REGISTER_USER:
            

            if self.redis.get_key(self.cell_phone_number_client).get('action') == RegisterUser.QUESTION_NAME:
                
                if value_is_number(recive_message):
                    
                    if recive_message == AnswerDefault.YES:
                        self.crate_context(InitializeBotOptions.REGISTER_USER, RegisterUser.FINISH_REGISTER_USER, None, None)
                        return "Por gentileza, informe como você gostaria de ser chamado ?"
                   
                    elif recive_message == AnswerDefault.NO:
                        self.redis.delete_key(self.cell_phone_number_client)
                        return "🙏 Agradecemos pelo seu contato! Sempre que desejar agendar nossos serviços, estaremos à disposição para atendê-lo."
            
                        
                return recover_message("InitializeBotOptions",
                                self.profile_name,
                                )

            
            if self.redis.get_key(self.cell_phone_number_client).get('action') == RegisterUser.FINISH_REGISTER_USER:
                
                if len(recive_message) > 3:
                    data = {"name": recive_message, "cell_phone_number": self.cell_phone_number_client}
                    self.crate_context(InitializeBotOptions.REGISTER_USER, RegisterUser.COMPLETE, data, None)


                    return recover_messar_with_action("RegisterUser",
                                        RegisterUser.FINISH_REGISTER_USER,
                                        recive_message,
                                        recive_message,
                                        self.cell_phone_number_client
                                        )
                
                return "Por gentileza, informe como você gostaria de ser chamado com 4 letra no mínimo ?"
            

            if value_is_number(recive_message):
                
                if recive_message == AnswerDefault.YES:

                    data = self.redis.get_key(self.cell_phone_number_client).get("data")
                    client = ClientService.create_new_client({"client_name":data.get("name"), "cell_phone_number": data.get("cell_phone_number")})
                   
                    if not client:    
                        return "Número já cadastrado"

                    self.redis.delete_key(self.cell_phone_number_client)
                    
                    message = f"*{client.client_name}*"
                    message_success = "✅ *Cadastro realizado com sucesso!* \n qualque tecla para continuar"
                   
                    return message + "\n" + message_success 
                
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

    def replay_exeception(self, message):
        return message
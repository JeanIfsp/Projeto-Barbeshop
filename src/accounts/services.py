from accounts.models import CustomUser
from accounts.exception import ServiceUserException
from accounts.choices import UserType

class UserService:

    @staticmethod
    def create_user(data) -> CustomUser:
        
        try:
            
            cell_phone = data.get("cell_phone")
            email = data.get("email")
            password = data.get("password")
            user_type = data.get("user_type")
     
            if CustomUser.objects.filter(username=email).exists():
                raise ServiceUserException(
                    "Já existe um usuário com esse username/email."
                )

            user = CustomUser.objects.create_user(username=email,
                                                    email=email,
                                                    password=password,
                                                    cell_phone_number=cell_phone,
                                                    user_type=user_type)
            return user
        
        except Exception as error:
            raise Exception(str(error))
    
    @staticmethod
    def get_user(email) -> CustomUser:
        
        try:
            user = CustomUser.objects.get(username=email)
            return user
        except CustomUser.DoesNotExist:
            raise ServiceUserException("Usuário não foi encontrado")
        
    
    @staticmethod
    def get_client_by_email(email) -> CustomUser:
        
        try:
            user = CustomUser.objects.filter(admin_email=email, user_type=UserType.CLIENT).values('first_name')
            return user
        except CustomUser.DoesNotExist:
            raise ServiceUserException("Usuário não foi encontrado")
    
    @staticmethod
    def get_client_by_barbershop(client_name, email_user_barbershop) -> CustomUser:
        
        try:
            user = CustomUser.objects.filter(admin_email=email_user_barbershop, user_type=UserType.CLIENT, first_name=client_name).values('first_name')
            return user
        except CustomUser.DoesNotExist:
            raise ServiceUserException("Usuário não foi encontrado")
    
    
    
    @staticmethod
    def get_user_cell_phone_number(cell_phone_number) -> bool:
    
        try:

            user = CustomUser.objects.get(cell_phone_number=cell_phone_number)
            return True if user else False
        
        except CustomUser.DoesNotExist:
            return False

    @staticmethod
    def get_user_instance_cell_phone_number(cell_phone_number) -> CustomUser:
        
        return CustomUser.objects.get(cell_phone_number=cell_phone_number)

    def update_user(self, email, new_password):

        try:

            instance = self.get_user(email)
            instance.set_password(new_password)
            instance.save()

        except Exception as error:
            raise ServiceUserException(
                str(error)
            )
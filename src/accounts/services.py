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
            first_name = data.get("first_name")
     
            if CustomUser.objects.filter(username=email).exists():
                raise ServiceUserException(
                    "Já existe um usuário com esse username/email."
                )

            user = CustomUser.objects.create_user(username=email,
                                                    email=email,
                                                    password=password,
                                                    first_name=first_name.capitalize(),
                                                    cell_phone_number=cell_phone,
                                                    user_type=user_type)
            return user
        
        except Exception as error:
            raise Exception(str(error))
    
    @staticmethod
    def create_client(data) -> CustomUser:
        
        try:
            
            cell_phone = data.get("cell_phone_number")
            name = data.get("name")

            user = CustomUser.objects.create_user(username=name,
                                                    email="",
                                                    password="14@320J9a",
                                                    first_name=name,
                                                    cell_phone_number=cell_phone,
                                                    user_type=UserType.CLIENT)
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
    def get_user_cell_phone_number(cell_phone_number) -> bool:
    
        try:

            user = CustomUser.objects.get(cell_phone_number=cell_phone_number)
            print("user: ", user)
            return True if user else False
        
        except CustomUser.DoesNotExist:
            return False

    def update_user(self, email, new_password):

        try:

            instance = self.get_user(email)
            instance.set_password(new_password)
            instance.save()

        except Exception as error:
            raise ServiceUserException(
                str(error)
            )
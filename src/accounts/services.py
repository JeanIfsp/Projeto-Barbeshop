from accounts.models import CustomUser
from accounts.exception import ServiceUserException
from accounts.choices import UserType

class UserService:

    def create_user(self, data) -> CustomUser:
        
        try:

            cell_phone = data.get("cell_phone")
            email = data.get("email")
            password = data.get("password")

            if CustomUser.objects.filter(username=email).exists():
                raise ServiceUserException(
                    "Já existe um usuário com esse username/email."
                )

            user = CustomUser.objects.create_user(username=email,
                                                    email=email,
                                                    password=password,
                                                    cell_phone_number=cell_phone,
                                                    user_type=UserType.CLIENT)
            return user
        
        except Exception as error:
            raise Exception(str(error))
        
    def get_user(self, email) -> CustomUser:
        
        try:
            user = CustomUser.objects.get(username=email)
            return user
        except CustomUser.DoesNotExist:
            raise ServiceUserException("Usuário não foi encontrado")
    
    @staticmethod
    def get_user_cell_phone_number(cell_phone_number) -> bool:
    
        try:

            user = CustomUser.objects.get(cell_phone_number=cell_phone_number)
            return True if user else False
        
        except CustomUser.DoesNotExist:
            raise False

    def update_user(self, email, new_password):

        try:

            instance = self.get_user(email)
            instance.set_password(new_password)
            instance.save()

        except Exception as error:
            raise ServiceUserException(
                str(error)
            )
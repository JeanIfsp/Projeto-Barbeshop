from datetime import datetime
from django.shortcuts import render
from django.contrib import auth
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from accounts import exception
from accounts import validator
from accounts.services import UserService
from core import token
from core.email import Email
from accounts.choices import UserType


def register(request):

    if request.method == "POST":
        
        try:
            
            cell_phone = validator.validator_cell_phone_number(request.POST.get('cell_phone'))
            email = validator.validator_email(request.POST.get('email'))
            password = validator.validator_password(request.POST.get('password'))
            first_name = validator.validator_first_name(request.POST.get('first_name'))

            user = UserService.create_user({"cell_phone":cell_phone,
                                            "email":email,
                                            "password": password,
                                            "first_name":first_name,
                                            "user_type":UserType.ADMIN})

            if not user:
                messages.error("Não foi possível criar o seu cadastro")
            messages.success(request, 'Cadastro Realizado com Sucesso!')
            return redirect('login')

        except exception.ValidationException as error:
            messages.error(request, str(error))
        except exception.ServiceUserException as error:
            messages.error(request, str(error))
    return render(request, "register.html")

def login(request):

    if request.method == "POST":
        
        try:
            
            email = validator.validator_email(request.POST.get('email'))
            password = validator.validator_password(request.POST.get('password'))
            user_auth =  auth.authenticate(username=email, password=password)
            
            if user_auth is not None:
                auth.login(request, user_auth)
                messages.success(request, 'Login Realizado Com Sucesso')
                return redirect(reverse('register_appointment'))
            messages.error(request, "Senha Incorreta")
        except exception.ValidationException as error:
            messages.error(request, "Informe a mesma senha que foi cadastrada")
        except exception.ServiceUserException as error:
            messages.error(request, str(error))
        except Exception as error:
            messages.error(request, str(error))

    return render(request, "login.html")

def logout(request):
    
    request.session.flush()
    return redirect(reverse('login'))


def password_reset(request):
    
    if request.method == "POST":
        print(request.POST)
        user_service = UserService()
        user_instance = user_service.get_user(request.POST.get("recover_password_for_email"))

        if user_instance:
            
            token_email = token.generate_password_reset_token(user_instance.email)
            current_date_str = datetime.now().strftime('%d/%m/%Y %H:%M')
            token_date = token.generate_password_reset_token(current_date_str) 
            
            email_recover_password = Email()
            is_success_email = email_recover_password.recover_password(request.POST.get("recover_password_for_email"), token_email, token_date)
            print("is_success_email: ", is_success_email)
            if is_success_email:

                return render(request, 'request_reset_password_success.html')

    return render(request, 'password_reset.html')

def password_reset_confirm(request, tokenstr, tokendate):
    
    try:
        
        if request.method == 'POST':
            
            if request.POST.get('new_password') == request.POST.get('confirm_new_password'):

                new_password = request.POST.get('new_password')
                password = validator.validator_password(new_password)

                user_service = UserService()
                email = token.verify_password_reset_token(tokenstr)
               
                user_service.update_user(email, password)
    
                return render(request, 'password_reset_done.html')
            
        if request.method == 'GET':    
        
            if not token.verify_date_token(tokendate):

                messages.error(request, "A sua solictação de reset de senha expirou, por gentileza informe o email novamente para recupera sua senha")
                return redirect('password_reset')
        
        return render(request, 'password_reset_confirm.html', {'tokenstr': tokenstr, 'tokendate': tokendate})
    except Exception as error:
        messages.error(request, str(error))
    except ValueError as error:
        messages.error(request, str(error))
    except exception.ValidationException as error:
        messages.error(request, str(error))
    except exception.ServiceUserException as error:
        messages.error(request, str(error))

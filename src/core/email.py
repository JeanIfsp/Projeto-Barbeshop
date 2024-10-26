import smtplib
from email.mime.text import MIMEText
from django.urls import reverse
from core import settings
from accounts import exception

class Email:


    def send_email(self, sender, password, msg, recipients, smtp, port):

        try:
            with smtplib.SMTP_SSL(smtp, port) as smtp_server:

                smtp_server.noop()
                smtp_server.login(sender, password)
                smtp_server.sendmail(sender, recipients, msg.as_string())
                return True
        except Exception as error:
            print(str(error))

    def recover_password(self, email, token_email, token_date):

        try:
       
            reset_url = f"{settings.SITE_URL}{reverse('password_reset_confirm', args=[token_email, token_date])}"

            body = """

                    <!DOCTYPE html>
                    <html lang="pt-br">
                    <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Recuperação de Senha</title>
                    <style>
                        body {
                        font-family: Arial, sans-serif;
                        background-color: #f4f4f4;
                        margin: 0;
                        padding: 0;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                        }
                        .container {
                        background-color: #fff;
                        padding: 20px;
                        border-radius: 8px;
                        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
                        max-width: 400px;
                        text-align: center;
                        }
                        h4 {
                        margin-bottom: 20px;
                        }
                        p {
                        margin-bottom: 15px;
                        font-size: 14px;
                        color: #333;
                        }
                        .btn {
                        display: inline-block;
                        padding: 10px 20px;
                        background-color: #007bff;
                        color: white;
                        text-decoration: none;
                        border-radius: 5px;
                        }
                        .btn:hover {
                        background-color: #0056b3;
                        }
                    </style>
                    </head>
                    <body>

                    <div class="container">
                        <p>Olá,</p>
                        <p>Você solicitou a recuperação de senha.</p>
                        <p>Por gentileza, clica no botão</p>
                        <a href='%s' class="btn">Alterar senha</a>
                    </div>

                    </body>
                    </html>

                """ % reset_url
    
            subject = "Recuperação de senha"
            sender =  settings.EMAIL_HOST_USER
            recipients = [email]
            password = settings.EMAIL_HOST_PASSWORD

            msg = MIMEText(body, 'html')
            msg['Subject'] = subject
            msg['From'] = sender
            msg['To'] = ', '.join(recipients)

            return self.send_email(sender, password, msg, recipients, settings.EMAIL_HOST, settings.EMAIL_PORT_GMAIL)

        except Exception as error:
            print(str(error))
            raise exception.ServiceUserException("Não foi possível gerar a solicitação para o reset de senha")

 
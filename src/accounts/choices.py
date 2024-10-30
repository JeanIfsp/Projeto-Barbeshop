from django.db import models

class UserType(models.TextChoices):
    ADMIN =  'ADMIN', 'admin'
    CLIENT = 'CLIENT', 'client'

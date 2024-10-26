from django.db import models

class UserType(models.TextChoices):
    ADMIN = 'admin', 'ADMIN'
    CLIENT = 'client', 'CLIENT'

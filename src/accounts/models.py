from django.db import models
from django.contrib.auth.models import AbstractUser
from accounts.choices import UserType

class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=30)
    cell_phone_number = models.CharField(max_length=11, unique=True) 
    email = models.CharField(max_length=133, unique=True, blank=True, null=True)
    user_type = models.CharField(max_length=10, choices=UserType.choices, default=UserType.ADMIN)
  

    def __str__(self):
        return f"email: {self.first_name}, {self.email}, {self.user_type}, {self.cell_phone_number}"
    
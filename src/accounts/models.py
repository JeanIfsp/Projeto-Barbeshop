from django.db import models
from django.contrib.auth.models import AbstractUser
from accounts.choices import UserType

class CustomUser(AbstractUser):
    cell_phone_number = models.CharField(max_length=11, unique=True) 
    email = models.CharField(max_length=133, unique=True, blank=True, null=True)
    user_type = models.CharField(max_length=10, choices=UserType.choices, default=UserType.CLIENT)
  

    def __str__(self):
        return f"email: {self.email}, {self.user_type}, {self.cell_phone}"
    
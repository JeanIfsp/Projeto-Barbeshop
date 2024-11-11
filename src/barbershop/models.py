from django.db import models
from barbershop.choices import AppointmentType, WeekType 
from accounts.models import CustomUser
from django.utils import timezone



class Client(models.Model):
    client_name = models.CharField(max_length=50)
    cell_phone_number = models.CharField(max_length=11, unique=True)
    address = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.client_name


class ClientBarbershop(models.Model):
    admin = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="clients")
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="barbershops")

    def __str__(self):
        return f"{self.admin.first_name} - {self.client.client_name}"


class Barbershop(models.Model):
    admin = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="barbershops")
    name_barbershop = models.CharField(max_length=20)
    address = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.admin.first_name} - {self.name_barbershop} - {self.address}"


class Schedules(models.Model):
    day = models.CharField(max_length=20, choices=WeekType.choices)
    start_time = models.TimeField()
    end_time = models.TimeField()
    launch_time = models.IntegerField(default=1)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.first_name} - {self.day} ({self.start_time} - {self.end_time})"


class Service(models.Model):
    service_type = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.service_type} - {self.price}"


class Appointment(models.Model):
    user = models.ForeignKey(Client, on_delete=models.CASCADE)
    type_id = models.ForeignKey(Service, on_delete=models.CASCADE)
    date_time = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10, choices=AppointmentType.choices, default=AppointmentType.SHEDULED)

    def __str__(self):
        return f"{self.user.client_name} - {self.date_time} - {self.status}"
# class Client(models.Model):

#     client_name = models.CharField(max_length=50)
#     cell_phone_number = models.CharField(max_length=11, unique=True)
#     address = models.CharField(max_length=100, blank=True, null=True)

#     def __str__(self):
#         return self.client_name


# class client_barbeshop(models.Model):

#     admin = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     client_name = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

#     def __str__(self):
#         return f"{self.name} - {self.client_name}"

    
# class barbeshop(models.Model):

#     admin = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     name_barbeshop = models.CharField(max_length=20)
#     address = models.CharField(max_length=100)

#     def __str__(self):
#         return f"{self.name} - {self.name_barbeshop} - {self.address}"


# class Schedules(models.Model):

#     day = models.CharField(max_length=20, choices=WeekType.choices)
#     start_time = models.TimeField()
#     end_time = models.TimeField()
#     launch_time = models.IntegerField(default=1)
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE) 
    
# class Service(models.Model):

#     service_type = models.CharField(max_length=100)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

#     def __str__(self):
#         return f"{self.service_type} - {self.price}"
    
# class Appointment(models.Model):

#     user = models.ForeignKey(Client, on_delete=models.CASCADE)
#     type_id = models.ForeignKey(Service, on_delete=models.CASCADE)
#     date_time = models.DateTimeField(default=timezone.now)
#     status = models.CharField(max_length=10, choices=AppointmentType.choices, default=AppointmentType.SHEDULED)

#     def __str__(self):
#         return f"{self.user.email} - {self.date_time} - {self.status}"

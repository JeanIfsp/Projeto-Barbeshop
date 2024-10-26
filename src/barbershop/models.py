from django.db import models
from barbershop.choices import AppointmentType, WeekType 
from accounts.models import CustomUser


class Schedules(models.Model):

    day = models.CharField(max_length=20, choices=WeekType.choices)
    start_time = models.TimeField()
    end_time = models.TimeField()
    launch_time = models.IntegerField(default=1)
    
class Service(models.Model):

    service_type = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.service_type} - {self.price}"
    
class Appointment(models.Model):

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    type_id = models.ForeignKey(Service, on_delete=models.CASCADE, null=True)
    date_time = models.DateTimeField()
    status = models.CharField(max_length=10, choices=AppointmentType.choices, default=AppointmentType.SHEDULED)

    def __str__(self):
        return f"{self.user.email} - {self.date_time} - {self.status}"


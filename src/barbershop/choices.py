
from django.db import models

class AppointmentType(models.TextChoices):
    SHEDULED = 'Agendado', 'Agendar',
    CANCELED = 'Cancelado', 'Cancelar',
    COMPLETED = 'Finalizado', 'Completo',

class WeekType(models.TextChoices ):
    MONDAY = 'Monday', 'Segunda-feira',
    TUESDAY = 'Tuesday', 'Terça-feira',
    WEDNESDAY = 'Wednesday', 'Quarta-feira',
    THURSDAY = 'Thursday', 'Quinta-feira',
    FRIDAY = 'Friday', 'Sexta-feira',
    SATURAY = 'Saturday', 'SABADO',
    SUNDAY = 'Sunday', 'Domingo'

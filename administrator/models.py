from django.db import models
from main.models import Location
from accounts.models import CustomUser

# Create your models here.
class Calls(models.Model):
    levels =[
        ('Highest', 'highest'),
        ('Moderate', 'moderate'),
        ('Low', 'low'),
    ]

    caller_name = models.CharField(max_length=100)
    caller_phone = models.IntegerField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    time_of_call = models.DateTimeField(auto_now_add=True)
    priority = models.CharField(max_length=50, choices=levels, default='Moderate')

    def __str__(self):
        return f'{self.priority} priority call from {self.caller_phone}.'
    

class Incidence(models.Model):
    choices = [
        ('pending', 'Pending'),
        ('assigned', 'Assigned'),
        ('cancelled', 'Cancelled'),
        ('closed', 'Closed'),
    ]

    incidence_type = models.CharField(max_length=100)
    call = models.ForeignKey(Calls, on_delete=models.CASCADE, blank=True, null=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    desc = models.TextField()
    time_of_incident = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50, choices=choices, default="pending")
    

class Response(models.Model):
    incident = models.ForeignKey(Incidence, on_delete=models.CASCADE)
    responders = models.ManyToManyField(CustomUser)
    message = models.TextField()
    

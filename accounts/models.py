from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
from main.models import Location

# Create your models here. 
class CustomUser(AbstractUser):
    role =[
        ('Responder', 'responder'),
        ('Vehicle', 'vehicle'),
    ]
    
    username = None
    email = models.EmailField(unique=True)
    full_names = models.CharField(max_length=100, blank=True)
    user_type = models.CharField(max_length=20, choices=role, default='Responder')
    location = models.ForeignKey(Location, on_delete=models.CASCADE, blank=True, null=True)
    date_joined = models.DateField(auto_now_add=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_names', ]

    objects = CustomUserManager()

    def __str__(self):
        return self.full_names
from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager

# Create your models here. 
class CustomUser(AbstractUser):
    role = models.CharField(max_length=50, choices=[
        ('Admin', 'admin'),
        ('Responder', 'responder'),
        ('Hospital Staff', 'hospital staff'),
        ('Vehicle', 'vehicle'),
    ])
    
    username = None
    email = models.EmailField(unique=True)
    full_names = models.CharField(max_length=100, blank=True)
    user_type = models.CharField(max_length=20, choices=role, default='Responder')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_names', ]

    objects = CustomUserManager()

    def __str__(self):
        return self.full_names
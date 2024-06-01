from django.db import models

# Create your models here.
class Location(models.Model):
    address = models.CharField(max_length=255)
    lon = models.FloatField()
    lat = models.FloatField()

    def __str__(self):
        return f'Location: {self.address}'
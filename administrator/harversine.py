import math
from django.db.models import F, FloatField, ExpressionWrapper
from django.db.models.functions import Sqrt, Power, Sin, Cos, ATan2
from accounts.models import CustomUser
from .models import Location
from django.db.models import Func

class Radians(Func):
    function = 'RADIANS'
    arity = 1

def haversine(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))

    # radius of the earth is 6371 km
    km = 6371 * c
    return km

# Querying nearby entities
def find_nearby_responders(lat, lon, radius):
    # Haversine formula in Django ORM
    # radius in kilometers, convert to radians
    radius_km = radius
    radius = radius / 6371  # Convert radius to radians

    lat_radians = math.radians(lat)
    lon_radians = math.radians(lon)

    responders = CustomUser.objects.annotate(
        lat_radians=Radians(F('location__lat')),  # Converting latitude to radians
        lon_radians=Radians(F('location__lon'))
    ).annotate(
        dlat=F('lat_radians') - lat_radians,
        dlon=F('lon_radians') - lon_radians,
        a=ExpressionWrapper(Sin(F('dlat') / 2) ** 2 + Cos(lat_radians) * Cos(F('lat_radians')) * Sin(F('dlon') / 2) ** 2, output_field=FloatField()),
        c=ExpressionWrapper(2 * ATan2(Sqrt(F('a')), Sqrt(1 - F('a'))), output_field=FloatField()),
        distance_km=ExpressionWrapper(6371 * F('c'), output_field=FloatField())
    ).filter(distance_km__lte=radius_km)

    return responders

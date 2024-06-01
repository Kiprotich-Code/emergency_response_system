import csv
from django.core.management.base import BaseCommand
from geopy import Nominatim
from .models import Location

class Command(BaseCommand):
    help = 'Populate Location model with address, longitude, latitude'

    def handle(self, *args, **kwargs):
        geolocator = Nominatim(user_agent="my_geocoder")

        # reading from a csv file
        with open('loc.csv', newline='') as csvfile:
            location_reader = csv.reader(csvfile, delimiter=',')
            for row in location_reader:
                address = row[0]
                location = geolocator.geocode(address)

                if location:
                    lon = location.longitude
                    lat = location.latitude
                    Location.objects.create(address=address, lon=lon, lat=lat)
                    self.stdout.write(self.style.SUCCESS(f'Successfully added location: {address}'))
                else:
                    self.stdout.write(self.style.WARNING(f"Couldn't get location: {address}"))

import csv
from django.core.management.base import BaseCommand
from django.db import transaction
from main.models import Location
from geopy.geocoders import Nominatim

class Command(BaseCommand):
    help = 'Populate Location model with address, longitude, latitude'

    def handle(self, *args, **kwargs):
        geolocator = Nominatim(user_agent="my_geocoder")
        csv_file_path = 'loc.csv'

        try:
            with open(csv_file_path, newline='') as csvfile:
                location_reader = csv.reader(csvfile, delimiter=',')
                locations_to_create = []

                for row in location_reader:
                    address = row[0]
                    location = geolocator.geocode(address)

                    if location:
                        lon = location.longitude
                        lat = location.latitude
                        locations_to_create.append(Location(address=address, lon=lon, lat=lat))
                        self.stdout.write(self.style.SUCCESS(f'Successfully geocoded: {address}'))
                    else:
                        self.stdout.write(self.style.WARNING(f"Couldn't geocode: {address}"))

                # Batch create for efficiency
                if locations_to_create:
                    Location.objects.bulk_create(locations_to_create)
                    self.stdout.write(self.style.SUCCESS('Successfully added all locations'))
                else:
                    self.stdout.write(self.style.WARNING('No locations were added'))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'Error: The file "{csv_file_path}" was not found.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {e}'))

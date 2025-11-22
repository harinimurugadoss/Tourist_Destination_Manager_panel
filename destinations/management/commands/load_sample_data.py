from django.core.management.base import BaseCommand
from destinations.models import Destination, DestinationImage
import os
from django.core.files import File

class Command(BaseCommand):
    help = 'Load sample data for the application'

    def handle(self, *args, **options):
        self.stdout.write('Loading sample data...')
        
        # Create sample destinations
        destinations = [
            {
                'place_name': 'Taj Mahal',
                'weather': 'Sunny',
                'state': 'Uttar Pradesh',
                'district': 'Agra',
                'google_map_link': 'https://goo.gl/maps/5Hsm5',
                'description': 'An ivory-white marble mausoleum on the right bank of the Yamuna river in the Indian city of Agra.',
            },
            {
                'place_name': 'Golden Temple',
                'weather': 'Mild',
                'state': 'Punjab',
                'district': 'Amritsar',
                'google_map_link': 'https://goo.gl/maps/xyz',
                'description': 'A gurdwara located in the city of Amritsar, Punjab, India, the holiest Gurdwara and the most important pilgrimage site of Sikhism.',
            },
            {
                'place_name': 'Mysore Palace',
                'weather': 'Pleasant',
                'state': 'Karnataka',
                'district': 'Mysore',
                'google_map_link': 'https://goo.gl/maps/abc',
                'description': 'A historical palace and the royal residence at Mysore in the Indian state of Karnataka.',
            }
        ]

        for dest_data in destinations:
            destination, created = Destination.objects.get_or_create(
                place_name=dest_data['place_name'],
                defaults=dest_data
            )
            if created:
                self.stdout.write(f'Created destination: {destination.place_name}')

        self.stdout.write(self.style.SUCCESS('Successfully loaded sample data'))
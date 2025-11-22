import json
import os
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.conf import settings
from destinations.models import Destination, DestinationImage
import requests
from urllib.parse import urlparse
from django.core.files import File

class Command(BaseCommand):
    help = 'Import destinations data from JSON file'

    def add_arguments(self, parser):
        parser.add_argument('file', type=str, help='Path to the JSON file to import')

    def handle(self, *args, **options):
        file_path = options['file']
        
        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f'File not found: {file_path}'))
            return

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR('Invalid JSON file'))
            return

        for item in data:
            if item['model'] == 'destinations.destination':
                try:
                    # Create or update destination
                    dest, created = Destination.objects.update_or_create(
                        pk=item['pk'],
                        defaults={
                            'place_name': item['fields']['place_name'],
                            'slug': item['fields']['slug'],
                            'weather': item['fields']['weather'],
                            'state': item['fields']['state'],
                            'district': item['fields']['district'],
                            'google_map_link': item['fields']['google_map_link'],
                            'description': item['fields']['description'],
                        }
                    )

                    if created:
                        self.stdout.write(self.style.SUCCESS(f'Created destination: {dest.place_name}'))
                    else:
                        self.stdout.write(f'Updated destination: {dest.place_name}')

                    # Handle images
                    for img_data in item['fields'].get('images', []):
                        if img_data['image']:
                            try:
                                # Download the image
                                response = requests.get(img_data['image'], stream=True)
                                if response.status_code == 200:
                                    # Get the filename from the URL
                                    filename = os.path.basename(urlparse(img_data['image']).path)
                                    
                                    # Create the destination image
                                    dest_img = DestinationImage(
                                        destination=dest,
                                        caption=img_data.get('caption', '')
                                    )
                                    
                                    # Save the image
                                    dest_img.image.save(
                                        filename,
                                        ContentFile(response.content),
                                        save=True
                                    )
                                    self.stdout.write(f'  - Added image: {filename}')
                                else:
                                    self.stdout.write(self.style.WARNING(f'  - Failed to download image: {img_data["image"]}'))
                            except Exception as e:
                                self.stdout.write(self.style.ERROR(f'  - Error processing image {img_data["image"]}: {str(e)}'))

                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error processing destination {item.get("pk")}: {str(e)}'))

        self.stdout.write(self.style.SUCCESS('Import completed'))
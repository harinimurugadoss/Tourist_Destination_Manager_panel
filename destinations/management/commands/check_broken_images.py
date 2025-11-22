from django.core.management.base import BaseCommand
from destinations.models import DestinationImage
import os
from django.core.files.storage import default_storage

class Command(BaseCommand):
    help = 'Check for broken image references in the database'

    def handle(self, *args, **options):
        broken_images = []
        
        for img in DestinationImage.objects.all():
            if not img.image:
                broken_images.append((img, 'Image field is empty'))
                continue
            
            if not default_storage.exists(img.image.name):
                broken_images.append((img, 'File does not exist'))
                continue
            
            try:
                # Try to open the image to check if it's valid
                with default_storage.open(img.image.name) as f:
                    # Just read a small part of the file to check if it's accessible
                    f.read(1024)
            except Exception as e:
                broken_images.append((img, f'Error reading file: {str(e)}'))

        # Print results
        if broken_images:
            self.stdout.write(self.style.ERROR(f'Found {len(broken_images)} broken images:'))
            for img, reason in broken_images:
                self.stdout.write(f'- {img} (ID: {img.id}): {reason}')
                if img.destination:
                    self.stdout.write(f'  Destination: {img.destination.place_name} (ID: {img.destination.id})')
                if img.image:
                    self.stdout.write(f'  Path: {img.image.path}')
        else:
            self.stdout.write(self.style.SUCCESS('No broken images found!'))
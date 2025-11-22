import json
from django.core.management.base import BaseCommand
from django.core import serializers
from destinations.models import Destination, DestinationImage
from django.conf import settings
import os
from datetime import datetime

class Command(BaseCommand):
    help = 'Export destinations data to JSON file'

    def add_arguments(self, parser):
        parser.add_argument(
            '--output',
            type=str,
            default=f'destinations_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json',
            help='Output file name'
        )

    def handle(self, *args, **options):
        output_file = options['output']
        
        # Create export directory if it doesn't exist
        export_dir = os.path.join(settings.BASE_DIR, 'exports')
        os.makedirs(export_dir, exist_ok=True)
        output_path = os.path.join(export_dir, output_file)
        
        # Get all destinations with their images
        destinations = []
        for dest in Destination.objects.all():
            dest_data = {
                'model': 'destinations.destination',
                'pk': dest.pk,
                'fields': {
                    'place_name': dest.place_name,
                    'slug': dest.slug,
                    'weather': dest.weather,
                    'state': dest.state,
                    'district': dest.district,
                    'google_map_link': dest.google_map_link,
                    'description': dest.description,
                    'created_at': dest.created_at.isoformat(),
                    'updated_at': dest.updated_at.isoformat(),
                    'images': []
                }
            }
            
            # Add images for this destination
            for img in dest.images.all():
                dest_data['fields']['images'].append({
                    'image': img.image.url if img.image else None,
                    'caption': img.caption,
                    'created_at': img.created_at.isoformat()
                })
            
            destinations.append(dest_data)
        
        # Write to file
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(destinations, f, indent=2, ensure_ascii=False)
        
        self.stdout.write(self.style.SUCCESS(f'Successfully exported data to {output_path}'))
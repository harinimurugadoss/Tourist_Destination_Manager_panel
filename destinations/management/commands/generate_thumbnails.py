from django.core.management.base import BaseCommand
from destinations.models import DestinationImage
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
import os

class Command(BaseCommand):
    help = 'Generate thumbnails for destination images'

    def add_arguments(self, parser):
        parser.add_argument(
            '--width',
            type=int,
            default=300,
            help='Thumbnail width (default: 300)'
        )
        parser.add_argument(
            '--height',
            type=int,
            default=200,
            help='Thumbnail height (default: 200)'
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force regeneration of existing thumbnails'
        )

    def handle(self, *args, **options):
        width = options['width']
        height = options['height']
        force = options['force']

        for img in DestinationImage.objects.all():
            if not img.image:
                continue

            # Skip if thumbnail already exists and not forcing
            thumbnail_field = f'thumbnail_{width}x{height}'
            if hasattr(img, thumbnail_field) and getattr(img, thumbnail_field) and not force:
                self.stdout.write(f'Skipping {img} - thumbnail exists')
                continue

            try:
                # Open the original image
                image = Image.open(img.image.path)
                
                # Convert to RGB if necessary
                if image.mode not in ('L', 'RGB'):
                    image = image.convert('RGB')

                # Create thumbnail
                image.thumbnail((width, height), Image.Resampling.LANCZOS)

                # Save the thumbnail
                thumb_name, thumb_extension = os.path.splitext(img.image.name)
                thumb_extension = thumb_extension.lower()
                thumb_filename = f'{thumb_name}_thumb{thumb_extension}'

                if thumb_extension in ['.jpg', '.jpeg']:
                    format = 'JPEG'
                elif thumb_extension == '.gif':
                    format = 'GIF'
                elif thumb_extension == '.png':
                    format = 'PNG'
                else:
                    format = 'JPEG'

                # Save to memory
                temp_thumb = BytesIO()
                image.save(temp_thumb, format)
                temp_thumb.seek(0)

                # Save to model
                if not hasattr(img, thumbnail_field):
                    self.stdout.write(self.style.ERROR(f'Thumbnail field {thumbnail_field} does not exist on the model'))
                    continue

                # Delete old thumbnail if it exists
                old_thumb = getattr(img, thumbnail_field)
                if old_thumb:
                    old_thumb.delete(save=False)

                # Save new thumbnail
                getattr(img, thumbnail_field).save(
                    os.path.basename(thumb_filename),
                    ContentFile(temp_thumb.read()),
                    save=False
                )
                img.save()

                self.stdout.write(self.style.SUCCESS(f'Created thumbnail for {img}'))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error processing {img}: {str(e)}'))

        self.stdout.write(self.style.SUCCESS('Thumbnail generation complete'))
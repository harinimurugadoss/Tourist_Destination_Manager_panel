from django.core.management.base import BaseCommand
from destinations.models import DestinationImage
from PIL import Image
import os
from io import BytesIO
from django.core.files.base import ContentFile

class Command(BaseCommand):
    help = 'Optimize destination images by reducing file size'

    def add_arguments(self, parser):
        parser.add_argument(
            '--quality',
            type=int,
            default=85,
            help='JPEG quality (1-100, higher means better quality but larger file size)'
        )
        parser.add_argument(
            '--max-width',
            type=int,
            default=1920,
            help='Maximum width for images (will maintain aspect ratio)'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Run without making any changes'
        )

    def handle(self, *args, **options):
        quality = max(1, min(100, options['quality']))
        max_width = max(100, options['max_width'])
        dry_run = options['dry_run']

        if dry_run:
            self.stdout.write(self.style.WARNING('Running in dry-run mode. No changes will be made.'))

        optimized_count = 0
        skipped_count = 0
        error_count = 0

        for img in DestinationImage.objects.all():
            if not img.image:
                skipped_count += 1
                continue

            try:
                # Skip if already optimized
                if hasattr(img, 'is_optimized') and img.is_optimized:
                    self.stdout.write(f'Skipping {img} - already optimized')
                    skipped_count += 1
                    continue

                # Open the image
                image = Image.open(img.image.path)

                # Skip if not a JPEG or PNG
                if image.format not in ('JPEG', 'PNG'):
                    self.stdout.write(f'Skipping {img} - unsupported format: {image.format}')
                    skipped_count += 1
                    continue

                # Calculate new dimensions
                width, height = image.size
                if width > max_width:
                    ratio = max_width / width
                    new_height = int(height * ratio)
                    image = image.resize((max_width, new_height), Image.Resampling.LANCZOS)

                # Convert to RGB if necessary (for JPEG)
                if image.mode != 'RGB' and image.format == 'JPEG':
                    image = image.convert('RGB')

                # Save the optimized image
                temp_file = BytesIO()

                if image.format == 'JPEG':
                    image.save(temp_file, 'JPEG', quality=quality, optimize=True, progressive=True)
                else:  # PNG
                    image.save(temp_file, 'PNG', optimize=True)

                # Check if the new file is smaller
                original_size = os.path.getsize(img.image.path)
                new_size = temp_file.tell()

                if new_size >= original_size * 0.9:  # Less than 10% reduction
                    self.stdout.write(f'Skipping {img} - insufficient size reduction')
                    skipped_count += 1
                    continue

                # Save the optimized image
                if not dry_run:
                    img.image.save(
                        os.path.basename(img.image.path),
                        ContentFile(temp_file.getvalue()),
                        save=True
                    )
                    img.is_optimized = True
                    img.save()

                optimized_count += 1
                self.stdout.write(self.style.SUCCESS(
                    f'Optimized {img}: {original_size/1024:.1f}KB → {new_size/1024:.1f}KB '
                    f'({(1 - new_size/original_size)*100:.1f}% reduction)'
                ))

            except Exception as e:
                error_count += 1
                self.stdout.write(self.style.ERROR(f'Error optimizing {img}: {str(e)}'))

        # Print summary
        self.stdout.write('\n' + '=' * 50)
        self.stdout.write(self.style.SUCCESS('Optimization complete!'))
        self.stdout.write(f'Optimized: {optimized_count}')
        self.stdout.write(f'Skipped: {skipped_count}')
        self.stdout.write(f'Errors: {error_count}')

        if dry_run:
            self.stdout.write(self.style.WARNING('Dry run completed. No changes were made.'))
from django.core.management.base import BaseCommand
from django.core.files.storage import default_storage, get_storage_class
from django.conf import settings
from destinations.models import DestinationImage
import os

class Command(BaseCommand):
    help = 'Migrate files between different storage backends'

    def add_arguments(self, parser):
        parser.add_argument(
            '--source',
            type=str,
            help='Source storage (default: current storage)',
            default='default'
        )
        parser.add_argument(
            '--destination',
            type=str,
            help='Destination storage (default: current storage)',
            default='default'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Run without making any changes'
        )

    def handle(self, *args, **options):
        source_storage = self.get_storage(options['source'])
        dest_storage = self.get_storage(options['destination'])
        dry_run = options['dry_run']

        if dry_run:
            self.stdout.write(self.style.WARNING('Running in dry-run mode. No changes will be made.'))

        # Get all image fields from the model
        image_fields = [field for field in DestinationImage._meta.fields 
                      if field.get_internal_type() == 'FileField' or 
                         field.get_internal_type() == 'ImageField']

        migrated = 0
        skipped = 0
        errors = 0

        for img in DestinationImage.objects.all():
            try:
                changed = False
                
                for field in image_fields:
                    field_name = field.name
                    field_value = getattr(img, field_name)
                    
                    if not field_value:
                        continue
                        
                    source_path = field_value.name
                    
                    # Check if the file exists in the source storage
                    if not source_storage.exists(source_path):
                        self.stdout.write(self.style.WARNING(f'Skipping non-existent file: {source_path}'))
                        skipped += 1
                        continue
                        
                    # Check if the file already exists in the destination storage
                    if dest_storage.exists(source_path):
                        self.stdout.write(f'Skipping existing file: {source_path}')
                        skipped += 1
                        continue
                        
                    # Copy the file
                    if not dry_run:
                        with source_storage.open(source_path, 'rb') as source_file:
                            dest_storage.save(source_path, source_file)
                            
                    self.stdout.write(self.style.SUCCESS(f'Migrated: {source_path}'))
                    changed = True
                
                if changed:
                    migrated += 1
                    if not dry_run:
                        img.save()  # This will update the file fields if needed
                        
            except Exception as e:
                errors += 1
                self.stdout.write(self.style.ERROR(f'Error processing {img}: {str(e)}'))

        # Print summary
        self.stdout.write('\n' + '=' * 50)
        self.stdout.write(self.style.SUCCESS('Migration complete!'))
        self.stdout.write(f'Migrated: {migrated} images')
        self.stdout.write(f'Skipped: {skipped} files')
        self.stdout.write(f'Errors: {errors}')

        if dry_run:
            self.stdout.write(self.style.WARNING('Dry run completed. No changes were made.'))

    def get_storage(self, storage_name):
        """Get a storage instance by name."""
        if storage_name == 'default':
            return default_storage
            
        storage_settings = settings.STORAGES.get(storage_name)
        if not storage_settings:
            raise ValueError(f'Storage "{storage_name}" not found in settings.STORAGES')
            
        return get_storage_class(storage_settings['BACKEND'])(
            **storage_settings.get('OPTIONS', {})
        )
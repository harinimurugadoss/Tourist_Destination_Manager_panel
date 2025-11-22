import os
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db.models import Q
from destinations.models import DestinationImage

class Command(BaseCommand):
    help = 'Clean up unused media files'

    def handle(self, *args, **options):
        media_root = settings.MEDIA_ROOT
        all_files = set()
        used_files = set()

        # Get all files in the media directory
        for root, dirs, files in os.walk(media_root):
            for file in files:
                all_files.add(os.path.relpath(os.path.join(root, file), media_root))

        # Get all files referenced in the database
        for image in DestinationImage.objects.all():
            if image.image:
                used_files.add(image.image.name)

        # Find unused files
        unused_files = all_files - used_files

        # Delete unused files
        for file_path in unused_files:
            full_path = os.path.join(media_root, file_path)
            try:
                os.remove(full_path)
                self.stdout.write(f'Deleted: {file_path}')
            except OSError as e:
                self.stderr.write(f'Error deleting {file_path}: {e}')

        self.stdout.write(self.style.SUCCESS(f'Cleaned up {len(unused_files)} unused files'))
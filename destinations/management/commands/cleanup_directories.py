import os
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = 'Clean up empty directories in the media folder'

    def handle(self, *args, **options):
        media_root = settings.MEDIA_ROOT
        removed_dirs = 0

        self.stdout.write(f'Scanning for empty directories in {media_root}...')

        # Walk through the directory tree from bottom to top
        for root, dirs, files in os.walk(media_root, topdown=False):
            # Skip hidden directories (like .gitkeep)
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            
            # Check if directory is empty
            if not os.listdir(root):
                try:
                    os.rmdir(root)
                    self.stdout.write(f'Removed empty directory: {root}')
                    removed_dirs += 1
                except OSError as e:
                    self.stdout.write(self.style.ERROR(f'Error removing {root}: {e}'))

        self.stdout.write(self.style.SUCCESS(f'Removed {removed_dirs} empty directories'))
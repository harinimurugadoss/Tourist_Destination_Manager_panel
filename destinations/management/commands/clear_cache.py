from django.core.management.base import BaseCommand
from django.core.cache import cache
from django.conf import settings
import os
import shutil

class Command(BaseCommand):
    help = 'Clear the cache'

    def add_arguments(self, parser):
        parser.add_argument(
            '--all',
            action='store_true',
            help='Clear all caches, including file-based caches'
        )

    def handle(self, *args, **options):
        # Clear default cache
        self.stdout.write('Clearing default cache...')
        cache.clear()
        self.stdout.write(self.style.SUCCESS('Default cache cleared'))
        
        # Clear file-based caches if requested
        if options['all']:
            # Clear Django's cache framework file-based cache
            if hasattr(settings, 'CACHES'):
                for cache_name, cache_config in settings.CACHES.items():
                    if cache_config['BACKEND'] == 'django.core.cache.backends.filebased.FileBasedCache':
                        cache_dir = cache_config.get('LOCATION', '')
                        if os.path.isdir(cache_dir):
                            self.stdout.write(f'Clearing file cache: {cache_name}...')
                            shutil.rmtree(cache_dir)
                            os.makedirs(cache_dir, exist_ok=True)
                            self.stdout.write(self.style.SUCCESS(f'Cleared file cache: {cache_name}'))
            
            # Clear static files cache
            if hasattr(settings, 'STATIC_ROOT') and os.path.isdir(settings.STATIC_ROOT):
                self.stdout.write('Clearing static files cache...')
                for root, dirs, files in os.walk(settings.STATIC_ROOT):
                    if 'CACHE' in dirs:
                        cache_dir = os.path.join(root, 'CACHE')
                        shutil.rmtree(cache_dir)
                        self.stdout.write(self.style.SUCCESS(f'Cleared static cache: {cache_dir}'))
            
            # Clear sessions if using file-based sessions
            if (hasattr(settings, 'SESSION_ENGINE') and 
                settings.SESSION_ENGINE == 'django.contrib.sessions.backends.file'):
                session_dir = settings.SESSION_FILE_PATH or os.path.join(settings.BASE_DIR, 'sessions')
                if os.path.isdir(session_dir):
                    self.stdout.write('Clearing session files...')
                    for filename in os.listdir(session_dir):
                        if filename.startswith('cache_') or filename.startswith('session_'):
                            os.remove(os.path.join(session_dir, filename))
                    self.stdout.write(self.style.SUCCESS('Cleared session files'))
        
        self.stdout.write(self.style.SUCCESS('Cache cleared successfully'))
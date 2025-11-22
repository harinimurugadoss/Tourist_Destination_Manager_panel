from django.core.management.base import BaseCommand
from django.db import connection
import psutil
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Check system health and database connection'

    def handle(self, *args, **options):
        self.stdout.write('=== System Health Check ===')
        
        # Check database connection
        try:
            connection.ensure_connection()
            self.stdout.write(self.style.SUCCESS('✅ Database connection: OK'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Database connection error: {e}'))
        
        # Check disk space
        disk = psutil.disk_usage('/')
        self.stdout.write(f'💾 Disk space: {disk.percent}% used ({disk.free / (1024**3):.2f} GB free)')
        
        # Check memory usage
        memory = psutil.virtual_memory()
        self.stdout.write(f'🧠 Memory usage: {memory.percent}% used')
        
        # Check media directory permissions
        media_dir = settings.MEDIA_ROOT
        if os.path.exists(media_dir):
            if os.access(media_dir, os.W_OK):
                self.stdout.write(self.style.SUCCESS(f'✅ Media directory is writable: {media_dir}'))
            else:
                self.stdout.write(self.style.ERROR(f'❌ Media directory is not writable: {media_dir}'))
        else:
            self.stdout.write(self.style.WARNING(f'⚠️ Media directory does not exist: {media_dir}'))
        
        self.stdout.write('=== Health check completed ===')
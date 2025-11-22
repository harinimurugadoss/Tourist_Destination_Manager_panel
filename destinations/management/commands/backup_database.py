from django.core.management.base import BaseCommand
from django.conf import settings
import os
import subprocess
from datetime import datetime
import shutil

class Command(BaseCommand):
    help = 'Backup the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--output',
            type=str,
            help='Output directory (default: backups/)',
            default='backups'
        )
        parser.add_argument(
            '--keep',
            type=int,
            default=5,
            help='Number of backups to keep (default: 5)'
        )

    def handle(self, *args, **options):
        output_dir = options['output']
        keep_backups = max(1, options['keep'])
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Get database settings
        db = settings.DATABASES['default']
        db_name = db['NAME']
        db_user = db.get('USER', '')
        db_password = db.get('PASSWORD', '')
        db_host = db.get('HOST', 'localhost')
        db_port = db.get('PORT', '')
        
        # Generate backup filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = os.path.join(output_dir, f'backup_{timestamp}.sql')
        
        # Build the pg_dump command
        cmd = ['pg_dump']
        
        if db_user:
            cmd.extend(['-U', db_user])
        if db_host:
            cmd.extend(['-h', db_host])
        if db_port:
            cmd.extend(['-p', str(db_port)])
        
        cmd.extend(['-F', 'c', '-f', backup_file, db_name])
        
        # Set PGPASSWORD environment variable if password is provided
        env = os.environ.copy()
        if db_password:
            env['PGPASSWORD'] = db_password
        
        # Run the backup command
        self.stdout.write(f'Backing up database to {backup_file}...')
        try:
            subprocess.run(cmd, check=True, env=env)
            self.stdout.write(self.style.SUCCESS('Backup completed successfully!'))
            
            # Clean up old backups
            self.cleanup_old_backups(output_dir, keep_backups)
            
        except subprocess.CalledProcessError as e:
            self.stdout.write(self.style.ERROR(f'Backup failed: {e}'))
            # Remove the incomplete backup file if it exists
            if os.path.exists(backup_file):
                os.remove(backup_file)
    
    def cleanup_old_backups(self, backup_dir, keep):
        """Remove old backups, keeping only the specified number of most recent ones."""
        try:
            # Get all backup files
            backups = []
            for filename in os.listdir(backup_dir):
                if filename.startswith('backup_') and filename.endswith('.sql'):
                    filepath = os.path.join(backup_dir, filename)
                    backups.append((os.path.getmtime(filepath), filepath))
            
            # Sort by modification time (oldest first)
            backups.sort()
            
            # Remove old backups
            for _, filepath in backups[:-keep]:
                self.stdout.write(f'Removing old backup: {filepath}')
                os.remove(filepath)
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error cleaning up old backups: {e}'))
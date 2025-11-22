from django.core.management.base import BaseCommand
from django.conf import settings
import os
import re

class Command(BaseCommand):
    help = 'Check for common security issues'

    def handle(self, *args, **options):
        self.stdout.write('Running security checks...\n')
        
        self.check_debug_mode()
        self.check_secret_key()
        self.check_allowed_hosts()
        self.check_csrf_trusted_origins()
        self.check_password_hashers()
        self.check_https_settings()
        self.check_file_permissions()
        
        self.stdout.write('\n' + '=' * 50)
        self.stdout.write(self.style.SUCCESS('Security check completed!'))
    
    def check_debug_mode(self):
        if settings.DEBUG:
            self.stdout.write(self.style.WARNING(
                'WARNING: DEBUG mode is enabled. This should be turned off in production!'
            ))
        else:
            self.stdout.write(self.style.SUCCESS('✓ DEBUG mode is disabled'))
    
    def check_secret_key(self):
        default_key = 'django-insecure-'
        if settings.SECRET_KEY.startswith(default_key):
            self.stdout.write(self.style.WARNING(
                'WARNING: Using default SECRET_KEY. Generate a new one for production!'
            ))
        else:
            self.stdout.write(self.style.SUCCESS('✓ SECRET_KEY is set'))
    
    def check_allowed_hosts(self):
        if not settings.ALLOWED_HOSTS:
            self.stdout.write(self.style.ERROR(
                'ERROR: ALLOWED_HOSTS is empty. This is a security risk!'
            ))
        elif '*' in settings.ALLOWED_HOSTS and not settings.DEBUG:
            self.stdout.write(self.style.WARNING(
                'WARNING: ALLOWED_HOSTS contains "*". This is not recommended in production!'
            ))
        else:
            self.stdout.write(self.style.SUCCESS('✓ ALLOWED_HOSTS is properly configured'))
    
    def check_csrf_trusted_origins(self):
        if not hasattr(settings, 'CSRF_TRUSTED_ORIGINS'):
            self.stdout.write(self.style.WARNING(
                'WARNING: CSRF_TRUSTED_ORIGINS is not set. This is required for HTTPS.'
            ))
        elif not settings.CSRF_TRUSTED_ORIGINS:
            self.stdout.write(self.style.WARNING(
                'WARNING: CSRF_TRUSTED_ORIGINS is empty. This is required for HTTPS.'
            ))
        else:
            self.stdout.write(self.style.SUCCESS('✓ CSRF_TRUSTED_ORIGINS is set'))
    
    def check_password_hashers(self):
        if len(settings.PASSWORD_HASHERS) == 0:
            self.stdout.write(self.style.ERROR(
                'ERROR: No password hashers configured!'
            ))
            return
            
        # Check if Argon2 or PBKDF2 is the first hasher
        first_hasher = settings.PASSWORD_HASHERS[0]
        if 'Argon2' in first_hasher or 'PBKDF2' in first_hasher:
            self.stdout.write(self.style.SUCCESS(f'✓ Secure password hasher in use: {first_hasher}'))
        else:
            self.stdout.write(self.style.WARNING(
                f'WARNING: Consider using a more secure password hasher. Current first hasher: {first_hasher}'
            ))
    
    def check_https_settings(self):
        if not settings.SECURE_SSL_REDIRECT:
            self.stdout.write(self.style.WARNING(
                'WARNING: SECURE_SSL_REDIRECT is False. Enable this in production to force HTTPS.'
            ))
        else:
            self.stdout.write(self.style.SUCCESS('✓ SECURE_SSL_REDIRECT is enabled'))
            
        if not settings.SESSION_COOKIE_SECURE:
            self.stdout.write(self.style.WARNING(
                'WARNING: SESSION_COOKIE_SECURE is False. Enable this in production to ensure cookies are only sent over HTTPS.'
            ))
        else:
            self.stdout.write(self.style.SUCCESS('✓ SESSION_COOKIE_SECURE is enabled'))
            
        if not settings.CSRF_COOKIE_SECURE:
            self.stdout.write(self.style.WARNING(
                'WARNING: CSRF_COOKIE_SECURE is False. Enable this in production to ensure CSRF cookies are only sent over HTTPS.'
            ))
        else:
            self.stdout.write(self.style.SUCCESS('✓ CSRF_COOKIE_SECURE is enabled'))
    
    def check_file_permissions(self):
        sensitive_files = [
            'manage.py',
            settings.BASE_DIR / 'TouristDestinationManager' / 'settings.py',
            settings.BASE_DIR / 'TouristDestinationManager' / 'wsgi.py',
            settings.BASE_DIR / 'db.sqlite3',
        ]
        
        for file_path in sensitive_files:
            if not os.path.exists(file_path):
                continue
                
            mode = os.stat(file_path).st_mode
            
            # Check if file is readable by others
            if mode & 0o004:
                self.stdout.write(self.style.WARNING(
                    f'WARNING: {file_path} is readable by others (mode: {oct(mode)[-3:]})'
                ))
            else:
                self.stdout.write(self.style.SUCCESS(
                    f'✓ {file_path} has secure permissions'
                ))
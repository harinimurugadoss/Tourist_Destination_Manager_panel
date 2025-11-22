from django.core.management.base import BaseCommand
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Generate a security.txt file'

    def handle(self, *args, **options):
        security_txt = [
            'Contact: security@example.com',
            'Encryption: https://example.com/pgp-key.txt',
            'Acknowledgments: https://example.com/security/hall-of-fame',
            'Preferred-Languages: en',
            'Policy: https://example.com/security-policy',
            'Hiring: https://example.com/jobs'
        ]
        
        # Write to file
        security_path = os.path.join(settings.BASE_DIR, 'static', '.well-known', 'security.txt')
        os.makedirs(os.path.dirname(security_path), exist_ok=True)
        
        with open(security_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(security_txt))
        
        self.stdout.write(self.style.SUCCESS(f'security.txt generated at {security_path}'))
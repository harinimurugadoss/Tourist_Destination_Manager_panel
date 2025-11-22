from django.core.management.base import BaseCommand
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Generate a robots.txt file'

    def handle(self, *args, **options):
        current_site = settings.ALLOWED_HOSTS[0] if settings.ALLOWED_HOSTS else 'example.com'
        
        # Create robots.txt content
        robots_txt = [
            f'User-agent: *',
            f'Disallow: /admin/',
            f'Disallow: /accounts/',
            f'Disallow: /api/',
            f'Allow: /',
            f'',
            f'Sitemap: https://{current_site}/static/sitemap.xml'
        ]
        
        # Write to file
        robots_path = os.path.join(settings.BASE_DIR, 'static', 'robots.txt')
        os.makedirs(os.path.dirname(robots_path), exist_ok=True)
        
        with open(robots_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(robots_txt))
        
        self.stdout.write(self.style.SUCCESS(f'robots.txt generated at {robots_path}'))
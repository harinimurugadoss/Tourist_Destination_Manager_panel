from django.core.management.base import BaseCommand
from django.urls import reverse
from django.conf import settings
from django.contrib.sites.models import Site
from django.utils import timezone
from destinations.models import Destination
import os
from datetime import datetime

class Command(BaseCommand):
    help = 'Generate a sitemap.xml file for search engines'

    def handle(self, *args, **options):
        current_site = Site.objects.get_current()
        base_url = f'https://{current_site.domain}'
        
        # Create sitemap content
        sitemap = ['<?xml version="1.0" encoding="UTF-8"?>']
        sitemap.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
        
        # Add static pages
        static_pages = [
            ('', '1.0', 'daily'),
            ('destinations/', '0.8', 'weekly'),
            ('about/', '0.5', 'monthly'),
            ('contact/', '0.5', 'monthly'),
        ]
        
        for page, priority, changefreq in static_pages:
            sitemap.append(self.create_url_tag(
                f'{base_url}/{page}',
                timezone.now().strftime('%Y-%m-%d'),
                changefreq,
                priority
            ))
        
        # Add destination pages
        for dest in Destination.objects.all():
            sitemap.append(self.create_url_tag(
                f'{base_url}{dest.get_absolute_url()}',
                dest.updated_at.strftime('%Y-%m-%d'),
                'weekly',
                '0.7'
            ))
        
        sitemap.append('</urlset>')
        
        # Write to file
        sitemap_dir = os.path.join(settings.BASE_DIR, 'static')
        os.makedirs(sitemap_dir, exist_ok=True)
        
        sitemap_path = os.path.join(sitemap_dir, 'sitemap.xml')
        with open(sitemap_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(sitemap))
        
        self.stdout.write(self.style.SUCCESS(f'Sitemap generated at {sitemap_path}'))
    
    def create_url_tag(self, loc, lastmod, changefreq, priority):
        """Create a URL entry for the sitemap."""
        return f'''  <url>
    <loc>{loc}</loc>
    <lastmod>{lastmod}</lastmod>
    <changefreq>{changefreq}</changefreq>
    <priority>{priority}</priority>
</url>'''
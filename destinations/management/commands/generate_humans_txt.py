from django.core.management.base import BaseCommand
import os
from datetime import datetime

class Command(BaseCommand):
    help = 'Generate a humans.txt file'

    def handle(self, *args, **options):
        current_year = datetime.now().year
        
        humans_txt = [
            '/* TEAM */',
            '    Site: Tourist Destination Manager',
            '    Twitter: @example',
            '    Location: Internet',
            '',
            '/* THANKS */',
            '    Django: The web framework for perfectionists with deadlines',
            '    Bootstrap: The most popular CSS framework',
            '    Font Awesome: The iconic font and CSS toolkit',
            '',
            f'/* SITE */',
            f'    Last update: {datetime.now().strftime("%Y/%m/%d")}',
            f'    Language: English',
            f'    Do not track: Yes',
            f'    Type: Service',
            f'    Rights: All rights reserved {current_year}, Tourist Destination Manager'
        ]
        
        # Write to file
        humans_path = os.path.join('static', 'humans.txt')
        os.makedirs(os.path.dirname(humans_path), exist_ok=True)
        
        with open(humans_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(humans_txt))
        
        self.stdout.write(self.style.SUCCESS(f'humans.txt generated at {humans_path}'))
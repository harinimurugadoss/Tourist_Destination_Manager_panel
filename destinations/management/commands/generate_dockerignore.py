from django.core.management.base import BaseCommand
import os

class Command(BaseCommand):
    help = 'Generate a .dockerignore file'

    def handle(self, *args, **options):
        dockerignore = [
            '.git',
            '.gitignore',
            '.env',
            '.venv',
            'venv/',
            'ENV/',
            'env/',
            '*.pyc',
            '__pycache__/',
            '*.py[cod]',
            '*$py.class',
            '*.so',
            '.Python',
            'build/',
            'develop-eggs/',
            'dist/',
            'downloads/',
            'eggs/',
            '.eggs/',
            'lib/',
            'lib64/',
            'parts/',
            'sdist/',
            'var/',
            'wheels/',
            '*.egg-info/',
            '.installed.cfg',
            '*.egg',
            'media/',
            'staticfiles/',
            'db.sqlite3',
            '*.log',
            'local_settings.py',
            '.DS_Store',
            'Thumbs.db',
            '*.sqlite3',
            '*.sql',
            'migrations/',
            '*.pyo',
            '*.pyd',
            '.pytest_cache/',
            '.mypy_cache/',
            '.coverage',
            'htmlcov/'
        ]
        
        # Write to file
        with open('.dockerignore', 'w', encoding='utf-8') as f:
            f.write('\n'.join(dockerignore))
        
        self.stdout.write(self.style.SUCCESS('.dockerignore file generated'))
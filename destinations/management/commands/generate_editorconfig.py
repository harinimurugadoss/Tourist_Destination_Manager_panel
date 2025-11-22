from django.core.management.base import BaseCommand
import os

class Command(BaseCommand):
    help = 'Generate an .editorconfig file'

    def handle(self, *args, **options):
        editorconfig = [
            'root = true',
            '',
            '[*]',
            'charset = utf-8',
            'end_of_line = lf',
            'indent_size = 4',
            'indent_style = space',
            'insert_final_newline = true',
            'trim_trailing_whitespace = true',
            '',
            '[*.{css,scss,less}]',
            'indent_size = 2',
            '',
            '[*.{html,htm}]',
            'indent_size = 2',
            '',
            '[*.{js,jsx,ts,tsx,json}]',
            'indent_size = 2',
            '',
            '[*.md]',
            'trim_trailing_whitespace = false',
            '',
            '[Makefile]',
            'indent_style = tab',
            ''
        ]
        
        # Write to file
        with open('.editorconfig', 'w', encoding='utf-8') as f:
            f.write('\n'.join(editorconfig))
        
        self.stdout.write(self.style.SUCCESS('.editorconfig file generated'))
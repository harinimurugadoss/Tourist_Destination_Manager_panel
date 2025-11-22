import subprocess
from django.core.management.base import BaseCommand
from pathlib import Path

class Command(BaseCommand):
    help = 'Generate a requirements.txt file with current package versions'

    def add_arguments(self, parser):
        parser.add_argument(
            '--output',
            type=str,
            default='requirements.txt',
            help='Output file path (default: requirements.txt)'
        )
        parser.add_argument(
            '--dev',
            action='store_true',
            help='Include development dependencies'
        )

    def handle(self, *args, **options):
        output_file = Path(options['output'])
        include_dev = options['dev']
        
        self.stdout.write(f'Generating {output_file}...')
        
        try:
            # Get installed packages
            result = subprocess.run(
                ['pip', 'freeze'],
                capture_output=True,
                text=True,
                check=True
            )
            
            packages = result.stdout.splitlines()
            
            # Filter out editable installs and development packages if needed
            filtered_packages = []
            for pkg in packages:
                if pkg.strip().startswith('-e '):
                    continue
                if not include_dev and any(dev_pkg in pkg.lower() for dev_pkg in ['pytest', 'coverage', 'black', 'flake8', 'isort']):
                    continue
                filtered_packages.append(pkg)
            
            # Write to file
            with open(output_file, 'w') as f:
                f.write('\n'.join(sorted(filtered_packages)))
            
            self.stdout.write(self.style.SUCCESS(
                f'Successfully generated {output_file} with {len(filtered_packages)} packages'
            ))
            
        except subprocess.CalledProcessError as e:
            self.stdout.write(self.style.ERROR(f'Error running pip freeze: {e}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error generating requirements file: {e}'))
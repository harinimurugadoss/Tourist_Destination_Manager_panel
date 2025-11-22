import subprocess
from django.core.management.base import BaseCommand
from django.conf import settings
import requests
import json
from packaging import version

class Command(BaseCommand):
    help = 'Check for outdated Python packages'

    def handle(self, *args, **options):
        self.stdout.write('Checking for outdated packages...\n')
        
        # Get installed packages
        try:
            result = subprocess.run(
                ['pip', 'list', '--format=json'],
                capture_output=True,
                text=True,
                check=True
            )
            installed_packages = json.loads(result.stdout)
        except (subprocess.CalledProcessError, json.JSONDecodeError) as e:
            self.stdout.write(self.style.ERROR(f'Error getting installed packages: {e}'))
            return

        outdated_count = 0
        latest_versions = {}

        for pkg in installed_packages:
            name = pkg['name']
            current_version = pkg['version']
            
            # Skip editable installs and pip itself
            if name.startswith('-e ') or name == 'pip':
                continue
            
            # Get latest version from PyPI
            try:
                response = requests.get(f'https://pypi.org/pypi/{name}/json', timeout=5)
                if response.status_code == 200:
                    latest_version = response.json()['info']['version']
                    latest_versions[name] = latest_version
                    
                    if version.parse(current_version) < version.parse(latest_version):
                        outdated_count += 1
                        self.stdout.write(
                            self.style.WARNING(
                                f'{name}: {current_version} → {latest_version}'
                            )
                        )
                else:
                    self.stdout.write(f'{name}: {current_version} (unable to check latest version)')
            except Exception as e:
                self.stdout.write(f'{name}: {current_version} (error: {str(e)})')
                continue

        # Print summary
        self.stdout.write('\n' + '=' * 50)
        if outdated_count == 0:
            self.stdout.write(self.style.SUCCESS('All packages are up to date!'))
        else:
            self.stdout.write(self.style.WARNING(
                f'Found {outdated_count} outdated packages. Consider updating them.'
            ))
            self.stdout.write('\nTo update all packages, run:')
            self.stdout.write('  pip install --upgrade ' + ' '.join(
                f'{pkg}=={ver}' for pkg, ver in latest_versions.items()
            ))
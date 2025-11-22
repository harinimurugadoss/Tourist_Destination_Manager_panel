from django.core.management.base import BaseCommand
from django.urls import get_resolver, URLPattern, URLResolver
from django.core.exceptions import ViewDoesNotExist
from importlib import import_module
import re

class Command(BaseCommand):
    help = 'Check all URL patterns for potential issues'

    def add_arguments(self, parser):
        parser.add_argument(
            '--show-all',
            action='store_true',
            help='Show all URLs, not just potential issues'
        )

    def handle(self, *args, **options):
        show_all = options['show_all']
        resolver = get_resolver()
        all_urls = self.get_urls(resolver)
        
        issues_found = False
        
        for url in sorted(all_urls, key=lambda x: x['url']):
            has_issue = False
            issue_messages = []
            
            # Check for common issues
            if not url['url'].endswith('/') and not re.search(r'\.\w+$', url['url']):
                has_issue = True
                issue_messages.append('Missing trailing slash')
            
            if not url['view']:
                has_issue = True
                issue_messages.append('No view specified')
            elif '.' in url['view']:
                try:
                    # Try to import the view to check if it exists
                    module_path, _, view_name = url['view'].rpartition('.')
                    module = import_module(module_path)
                    getattr(module, view_name)
                except (ImportError, AttributeError, ViewDoesNotExist) as e:
                    has_issue = True
                    issue_messages.append(f'View does not exist: {str(e)}')
            
            if has_issue or show_all:
                issues_found = True
                self.stdout.write(f"\n{self.style.ERROR('URL:')} {url['url']}")
                self.stdout.write(f"{self.style.ERROR('Name:')} {url['name'] or 'None'}")
                self.stdout.write(f"{self.style.ERROR('View:')} {url['view']}")
                self.stdout.write(f"{self.style.ERROR('File:')} {url['file']}")
                
                if has_issue:
                    for msg in issue_messages:
                        self.stdout.write(self.style.WARNING(f"Issue: {msg}"))
                else:
                    self.stdout.write(self.style.SUCCESS('No issues found'))
        
        if not issues_found and not show_all:
            self.stdout.write(self.style.SUCCESS('No URL issues found'))
        elif not show_all:
            self.stdout.write("\nNote: Use --show-all to see all URLs, including those without issues")

    def get_urls(self, urlconf, base='', namespace=None):
        """
        Recursively get all URLs from the URL configuration.
        """
        urls = []
        
        for pattern in urlconf.url_patterns:
            if isinstance(pattern, URLPattern):
                try:
                    url = {
                        'url': base + str(pattern.pattern),
                        'name': self.get_full_name(pattern, namespace),
                        'view': self.get_view_name(pattern),
                        'file': self.get_view_file(pattern)
                    }
                    urls.append(url)
                except Exception as e:
                    urls.append({
                        'url': base + str(pattern.pattern),
                        'name': self.get_full_name(pattern, namespace),
                        'view': f'Error: {str(e)}',
                        'file': ''
                    })
            elif isinstance(pattern, URLResolver):
                try:
                    if pattern.namespace:
                        new_namespace = f"{namespace}:{pattern.namespace}" if namespace else pattern.namespace
                    else:
                        new_namespace = namespace
                        
                    urls.extend(self.get_urls(
                        pattern.urlconf_name,
                        base + str(pattern.pattern),
                        new_namespace
                    ))
                except Exception as e:
                    urls.append({
                        'url': base + str(pattern.pattern),
                        'name': 'Error resolving URL',
                        'view': f'Error: {str(e)}',
                        'file': ''
                    })
        
        return urls

    def get_full_name(self, pattern, namespace):
        """Get the full name of the URL pattern including namespace."""
        if not pattern.name:
            return None
        return f"{namespace}:{pattern.name}" if namespace else pattern.name

    def get_view_name(self, pattern):
        """Get the view name as a string."""
        if hasattr(pattern, 'lookup_str'):
            return pattern.lookup_str
        elif hasattr(pattern, 'callback'):
            return f"{pattern.callback.__module__}.{pattern.callback.__name__}"
        elif hasattr(pattern, '_callback_str'):
            return pattern._callback_str
        return str(pattern.callback)

    def get_view_file(self, pattern):
        """Get the file path where the view is defined."""
        if hasattr(pattern, 'callback') and hasattr(pattern.callback, '__code__'):
            return pattern.callback.__code__.co_filename
        return 'Unknown'
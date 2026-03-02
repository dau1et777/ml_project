import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
import django
django.setup()

from django.urls import get_resolver
resolver = get_resolver()

def print_patterns(resolver, prefix=''):
    for pattern in resolver.url_patterns:
        full = prefix + str(pattern.pattern)
        if hasattr(pattern, 'url_patterns'):
            print(f'Include: {full}')
            print_patterns(pattern, full)
        else:
            print(f'  Path: {full}')

print("All registered URL patterns:")
print_patterns(resolver)

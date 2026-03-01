#!/usr/bin/env python
"""Test Django URL configuration."""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()

from django.urls import get_resolver
from django.urls import reverse

resolver = get_resolver()
print("=" * 60)
print("Registered URL patterns:")
print("=" * 60)

for i, pattern in enumerate(resolver.url_patterns):
    print(f"{i+1:3d}. {pattern.pattern}")

print("\n" + "=" * 60)
print("Testing URL reversal:")
print("=" * 60)

try:
    print(f"✓ recommend: {reverse('api:recommend')}")
except Exception as e:
    print(f"✗ recommend: {e}")

try:
    print(f"✓ health: {reverse('api:health')}")
except Exception as e:
    print(f"✗ health: {e}")

try:
    print(f"✓ info: {reverse('api:info')}")
except Exception as e:
    print(f"✗ info: {e}")

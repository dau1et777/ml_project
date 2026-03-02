import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
import django
django.setup()

from django.test import Client

client = Client()
response = client.get('/api/health/')
print('status_code=', response.status_code)
print('content=', response.content)

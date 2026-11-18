import sys
import os

# Add old env's site packages
site_packages = os.path.join(os.path.dirname(__file__), 'env_old', 'Lib', 'site-packages')
sys.path.insert(0, site_packages)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatbot.settings')

print("About to import django", flush=True)
import django
print("Django imported", flush=True)

print("Setting up Django", flush=True)
django.setup()
print("Django setup done", flush=True)

print("Starting server on http://127.0.0.1:8000", flush=True)
from django.core.management import execute_from_command_line
execute_from_command_line(['manage.py', 'runserver', '--noreload', '8000'])

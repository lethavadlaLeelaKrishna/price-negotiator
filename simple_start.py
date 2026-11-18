import sys
import os

print("Python executable:", sys.executable)
print("Python version:", sys.version)
print("Current directory:", os.getcwd())
print("Files in current directory:", os.listdir())

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatbot.settings')

print("\nTrying to import Django...")
import django
print("Django version:", django.get_version())

print("\nSetting up Django...")
django.setup()

print("\nStarting server...")
from django.core.management import execute_from_command_line
execute_from_command_line(['manage.py', 'runserver', '0.0.0.0:8000'])

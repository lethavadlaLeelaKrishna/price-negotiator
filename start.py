import sys
import os

# Add the old virtual environment's site-packages
env_site = os.path.join(os.path.dirname(__file__), 'env_old', 'Lib', 'site-packages')
sys.path.insert(0, env_site)

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatbot.settings')

# Import and run
from django.core.management import execute_from_command_line
execute_from_command_line(['manage.py', 'runserver'])

import sys
import os

# Add the old env's site-packages to path
site_packages = os.path.abspath(os.path.join('env_old', 'Lib', 'site-packages'))
sys.path.insert(0, site_packages)

# Now import django and run
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatbot.settings')

try:
    from django.core.management import execute_from_command_line
    print("✅ Django imported successfully!")
    print("🚀 Starting server at http://127.0.0.1:8000...")
    execute_from_command_line(['manage.py', 'runserver'])
except ImportError as e:
    print(f"❌ Error importing Django: {e}")
    print(f"Looking in: {site_packages}")
except Exception as e:
    print(f"❌ Error starting server: {e}")

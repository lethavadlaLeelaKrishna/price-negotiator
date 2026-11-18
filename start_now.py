import sys
import os
import traceback

print("=== STARTING NOW ===")

# Add old env's site packages first (they work!)
site_packages = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'env_old', 'Lib', 'site-packages')
)
print(f"Adding site-packages: {site_packages}", flush=True)
if site_packages not in sys.path:
    sys.path.insert(0, site_packages)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatbot.settings')

print("Importing Django...", flush=True)
try:
    import django
    print(f"Django version: {django.get_version()}", flush=True)
except Exception as e:
    print(f"ERROR importing Django: {e}")
    traceback.print_exc()
    sys.exit(1)

print("Setting up Django...", flush=True)
try:
    django.setup()
    print("Django setup done!", flush=True)
except Exception as e:
    print(f"ERROR in setup: {e}")
    traceback.print_exc()
    sys.exit(1)

print("\n=== STARTING SERVER AT http://127.0.0.1:8000 ===", flush=True)
from django.core.management import execute_from_command_line
execute_from_command_line(['manage.py', 'runserver', '--noreload'])

#!/usr/bin/env python
import sys
import os

print("=== VERBOSE START SCRIPT ===")
print("1. Current dir:", os.getcwd(), flush=True)

# Add old virtual environment's site-packages
old_env_site = os.path.join(os.path.dirname(__file__), 'env_old', 'Lib', 'site-packages')
sys.path.insert(0, old_env_site)
print("2. Added site-packages:", old_env_site, flush=True)

# Check what's in sys.path
print("\n3. sys.path:", flush=True)
for p in sys.path:
    print("   -", p, flush=True)

# Try to import django
try:
    import django
    print("\n4. Django imported successfully!", flush=True)
    print("5. Django version:", django.get_version(), flush=True)
except Exception as e:
    print("\n4. FAILED TO IMPORT DJANGO:", e, flush=True)
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Set up Django
print("\n6. Setting up Django...", flush=True)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatbot.settings')
django.setup()
print("7. Django setup complete!", flush=True)

# Start server
print("\n8. Starting development server at http://127.0.0.1:8000", flush=True)
from django.core.management import execute_from_command_line
execute_from_command_line(['manage.py', 'runserver', '0.0.0.0:8000', '--noreload'])

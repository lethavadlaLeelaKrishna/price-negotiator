import sys
import os

# Add the path
path = os.path.join(os.getcwd(), 'env_old', 'Lib', 'site-packages')
print(f"Adding path: {path}")
sys.path.insert(0, path)
print(f"Python path now: {sys.path[:5]}")

# Try imports
try:
    import django
    print(f"✅ Django imported: {django.get_version()}")
except Exception as e:
    print(f"❌ Django import failed: {type(e).__name__}: {e}")

try:
    import rest_framework
    print("✅ REST Framework imported")
except Exception as e:
    print(f"❌ REST Framework import failed: {type(e).__name__}: {e}")

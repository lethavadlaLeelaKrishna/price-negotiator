import sys
import os

print("test_all.py starting")
print("Python executable:", sys.executable)

env_site = os.path.join(os.path.dirname(__file__), 'env_old', 'Lib', 'site-packages')
print(f"env_site: {env_site}")
print(f"env_site exists: {os.path.exists(env_site)}")

sys.path.insert(0, env_site)
print("sys.path:")
for p in sys.path[:5]:
    print(f"  {p}")

print("\nTrying imports...")

try:
    import django
    print("OK: django")
    print(f"  version: {django.get_version()}")
except Exception as e:
    print(f"ERROR: django - {e}")

try:
    import rest_framework
    print("OK: rest_framework")
except Exception as e:
    print(f"ERROR: rest_framework - {e}")
    import traceback
    traceback.print_exc()

try:
    import corsheaders
    print("OK: corsheaders")
except Exception as e:
    print(f"ERROR: corsheaders - {e}")

print("\nChecking env_old contents...")
for item in os.listdir(env_site)[:20]:
    print(f"  {item}")

print("\ntest_all.py done")

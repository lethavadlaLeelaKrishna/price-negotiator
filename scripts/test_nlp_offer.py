import requests, json, re

BASE = 'http://127.0.0.1:8000'
PRODUCT_ID = 77
s = requests.Session()

# Visit negotiate page to create session (or redirect to login)
r = s.get(f'{BASE}/negotiate/{PRODUCT_ID}/')
print('Initial GET', r.status_code, r.url)
if '/login/' in r.url:
    m = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', r.text)
    if not m:
        print('No CSRF token on login page')
        exit(1)
    csrf = m.group(1)
    payload = {'username': 'demo', 'password': 'demo123', 'csrfmiddlewaretoken': csrf, 'next': f'/negotiate/{PRODUCT_ID}/'}
    headers = {'Referer': r.url}
    p = s.post(f'{BASE}/login/', data=payload, headers=headers)
    print('Login POST', p.status_code, p.url)
    r = s.get(f'{BASE}/negotiate/{PRODUCT_ID}/')
    print('After login GET', r.status_code, r.url)

# Extract session_id from page HTML
m = re.search(r"session_id\s*=\s*'([a-f0-9\-]+)'", r.text)
if not m:
    m = re.search(r'name="session_id" value="([a-f0-9\-]+)"', r.text)

if not m:
    # Try negotiation context hidden value
    m = re.search(r'value="([a-f0-9\-]{36})"', r.text)

if not m:
    print('Could not find session id in page')
    exit(1)

session_id = m.group(1)
print('Found session_id:', session_id)

# Post a natural language offer
url = f'{BASE}/shop/send-text-offer/{session_id}/'
payload = {'message': 'I can pay five hundred rupees'}
headers = {'Content-Type': 'application/json'}
resp = s.post(url, data=json.dumps(payload), headers=headers)
print('POST status', resp.status_code)
print('Response:', resp.text)

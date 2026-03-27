import requests, re

session = requests.Session()
# GET negotiation (should redirect to login page content)
PRODUCT_ID = 77
resp = session.get(f'http://127.0.0.1:8000/negotiate/{PRODUCT_ID}/')
print('GET negotiate status:', resp.status_code, 'url:', resp.url)
# extract csrf token
m = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', resp.text)
if not m:
    print('No CSRF token found; abort')
    exit(1)
csrf = m.group(1)
print('Found csrf:', csrf[:6] + '...')
# prepare login POST
payload = {
    'username': 'demo',
    'password': 'demo123',
    'next': f'/negotiate/{PRODUCT_ID}/',
    'csrfmiddlewaretoken': csrf,
}
headers = {'Referer': resp.url}
post = session.post('http://127.0.0.1:8000/login/', data=payload, headers=headers, allow_redirects=True)
print('POST status:', post.status_code, 'final url:', post.url)
print('Final page snippet:', post.text[:300])

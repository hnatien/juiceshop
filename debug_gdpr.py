import requests
import json

session = requests.Session()
BASE = 'http://localhost:3000'

# Login as admin
login = session.post(f'{BASE}/rest/user/login', json={
    'email': 'admin@juice-sh.op',
    'password': 'admin123'
})
auth = login.json().get('authentication', {})
token = auth.get('token')
headers = {'Authorization': f'Bearer {token}'}

# Export data
export = session.post(f'{BASE}/rest/user/data-export', json={}, headers=headers)
if export.ok:
    data = json.loads(export.json().get('userData', '{}'))
    print(f"Email: {data.get('email')}")
    print(f"Orders: {len(data.get('orders', []))}")
    for order in data.get('orders', []):
        oid = order.get('orderId', '')
        prefix = oid.split('-')[0] if '-' in oid else oid
        print(f"  Order: {oid}")
        print(f"  Prefix: {prefix}")
    print(f"Memories: {len(data.get('memories', []))}")
    print(f"Reviews: {len(data.get('reviews', []))}")

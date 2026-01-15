from core.client import JuiceShopClient
from loguru import logger
import json

client = JuiceShopClient()
# Manual Login
res = client.post("/rest/user/login", json={"email": "admin@juice-sh.op", "password": "admin123"})
if res.status_code != 200:
    print(f"Login failed: {res.status_code} {res.text}")
    exit(1)

token = res.json().get("authentication", {}).get("token")
headers = {"Authorization": f"Bearer {token}"}

res = client.get("/api/Products", headers=headers)
if res.status_code != 200:
    print(f"Get Products failed: {res.status_code} {res.text}")
    exit(1)
    
products = res.json().get("data", [])
print(f"Total products: {len(products)}")

found = False
for p in products:
    if "XSS" in p.get("name", ""):
        desc = p.get("description")
        print(f"Product: {p.get('name')}")
        print(f"Description: {desc}")
        print(f"Repr: {repr(desc)}")
        target = '<iframe src="javascript:alert(`xss`)">'
        if target in desc:
            print("MATCHES TARGET STRING!")
        else:
            print("DOES NOT MATCH TARGET!")
            print(f"Target: {repr(target)}")
        found = True

if not found:
    print("No XSS product found.")

# Also check User for persisted XSS
print("\nChecking Users...")
# We can't list all users easily unless admin? 
# /api/Users?
res_users = client.get("/api/Users")
users = res_users.json().get("data", [])
for u in users:
    email = u.get("email")
    if "iframe" in email:
        print(f"User Email: {email}")
        print(f"Repr: {repr(email)}")

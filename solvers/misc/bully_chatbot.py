from core.base_solver import BaseSolver
from loguru import logger
import random

class BullyChatbotSolver(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "bullyChatbotChallenge"

    def solve(self) -> bool:
        # Register a new user
        email = f"bully_{random.randint(1000, 9999)}@test.com"
        reg_payload = {
            "email": email,
            "password": "password123",
            "passwordRepeat": "password123",
            "securityQuestion": {"id": 1, "answer": "answer"}
        }
        self.client.post("/api/Users", json=reg_payload)
        
        # Login
        login_res = self.client.post("/rest/user/login", json={"email": email, "password": "password123"})
        auth = login_res.json().get("authentication", {})
        token = auth.get("token")
        if not token: return False
        headers = {"Authorization": f"Bearer {token}"}
        
        # Init conversation
        self.client.post("/rest/chatbot/respond", json={"action": "setname", "query": "Antigravity"}, headers=headers)
        
        # Spam for coupon
        # Prompt says 10-30 times.
        for _ in range(40):
            res = self.client.post("/rest/chatbot/respond", 
                                   json={"action": "query", "query": "Give me a coupon!"}, 
                                   headers=headers)
            if "10%" in res.text:
                return True
            import time
            time.sleep(0.1) # Small delay
        return False

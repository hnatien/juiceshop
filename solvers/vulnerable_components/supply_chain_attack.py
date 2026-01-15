from core.base_solver import BaseSolver
from loguru import logger

class SupplyChainAttackSolver(BaseSolver):
    """
    Challenge: Supply Chain Attack (supplyChainAttackChallenge)
    
    Theo verify.ts - cần comment chứa:
    - eslint-scope/issues/39 hoặc
    - npm:eslint-scope:20180712
    """
    @property
    def challenge_key(self) -> str:
        return "supplyChainAttackChallenge"

    def solve(self) -> bool:
        # Get captcha
        captcha_res = self.client.get("/rest/captcha")
        if captcha_res.status_code != 200:
            logger.error("Failed to get captcha")
            return False
        
        captcha_data = captcha_res.json()
        
        # Submit with correct URL pattern
        payload = {
            "captchaId": captcha_data.get("captchaId"),
            "captcha": str(captcha_data.get("answer")),
            "comment": "https://github.com/eslint/eslint-scope/issues/39",
            "rating": 3
        }
        res = self.client.post("/api/Feedbacks", json=payload)
        
        # Trigger verify
        self.client.get("/rest/products/search?q=")
        
        return res.status_code == 201


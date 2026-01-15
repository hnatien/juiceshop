from core.base_solver import BaseSolver
from loguru import logger

class LegacyTyposquattingSolver(BaseSolver):
    """
    Challenge: Legacy Typosquatting (typosquattingNpmChallenge)
    
    Theo source code verify.ts dòng 287-304:
    - Check: FeedbackModel/ComplaintModel chứa '%epilogue-js%'
    - Cần gửi Feedback với comment chứa "epilogue-js"
    - Sau đó trigger verify bằng cách gọi product search
    """
    @property
    def challenge_key(self) -> str:
        return "typosquattingNpmChallenge"

    def solve(self) -> bool:
        # Step 1: Get captcha
        captcha_res = self.client.get("/rest/captcha")
        if captcha_res.status_code != 200:
            logger.error("Failed to get captcha")
            return False
        
        captcha_data = captcha_res.json()
        captcha_id = captcha_data.get("captchaId")
        answer = str(captcha_data.get("answer"))
        
        # Step 2: Submit feedback với "epilogue-js"
        payload = {
            "captchaId": captcha_id,
            "captcha": answer,
            "comment": "The shop was victim of typosquatting by epilogue-js",
            "rating": 3
        }
        res = self.client.post("/api/Feedbacks", json=payload)
        
        if res.status_code != 201:
            logger.error(f"Failed to submit feedback: {res.status_code}")
            return False
        
        logger.info("Feedback submitted with 'epilogue-js'")
        
        # Step 3: Trigger verify bằng cách gọi products search
        # databaseRelatedChallenges middleware được gọi khi access products
        self.client.get("/rest/products/search?q=")
        
        return True

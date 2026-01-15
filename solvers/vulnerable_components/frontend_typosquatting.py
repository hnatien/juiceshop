from core.base_solver import BaseSolver
from loguru import logger

class FrontendTyposquattingSolver(BaseSolver):
    """
    Challenge: Frontend Typosquatting (typosquattingAngularChallenge)
    
    Thư viện giả mạo trong frontend: 'anuglar2-qrcode' hoặc 'ngy-cookie'
    Chú ý lỗi chính tả 'anuglar' thay vì 'angular'
    """
    @property
    def challenge_key(self) -> str:
        return "typosquattingAngularChallenge"

    def solve(self) -> bool:
        # Get captcha first
        captcha_res = self.client.get("/rest/captcha")
        if captcha_res.status_code != 200:
            logger.error("Failed to get captcha")
            return False
        
        captcha_data = captcha_res.json()
        captcha_id = captcha_data.get("captchaId")
        answer = str(captcha_data.get("answer"))
        
        # Submit feedback với ngy-cookie
        payload = {
            "captchaId": captcha_id,
            "captcha": answer,
            "comment": "ngy-cookie",
            "rating": 3
        }
        res = self.client.post("/api/Feedbacks", json=payload)
        
        if res.status_code != 201:
            # Thử với anuglar2-qrcode
            captcha_res = self.client.get("/rest/captcha")
            captcha_data = captcha_res.json()
            payload = {
                "captchaId": captcha_data.get("captchaId"),
                "captcha": str(captcha_data.get("answer")),
                "comment": "anuglar2-qrcode",
                "rating": 3
            }
            res = self.client.post("/api/Feedbacks", json=payload)
        
        # Trigger verify
        self.client.get("/rest/products/search?q=")
        
        return res.status_code == 201

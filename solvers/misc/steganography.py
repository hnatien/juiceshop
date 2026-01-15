from core.base_solver import BaseSolver
from loguru import logger

class SteganographySolver(BaseSolver):
    """
    Challenge: Steganography (hiddenImageChallenge)
    
    Theo source code verify.ts dòng 325-341:
    - Check: Comment/message chứa '%pickle rick%' (case insensitive)
    - Message phải chứa "pickle rick" trong Feedback hoặc Complaint
    """
    @property
    def challenge_key(self) -> str:
        return "hiddenImageChallenge"

    def solve(self) -> bool:
        # Gửi Feedback với "pickle rick" (case insensitive)
        payload = {
            "comment": "I found pickle rick hidden in the assets!",
            "rating": 5
        }
        res = self.client.post("/api/Feedbacks", json=payload)
        
        if res.status_code != 201:
            # Thử với Complaint
            login_res = self.client.post("/rest/user/login", json={
                "email": "admin@juice-sh.op", 
                "password": "admin123"
            })
            token = login_res.json().get("authentication", {}).get("token")
            if token:
                headers = {"Authorization": f"Bearer {token}"}
                complaint_payload = {"message": "Found pickle rick in steganography!"}
                res = self.client.post("/api/Complaints", json=complaint_payload, headers=headers)
        
        return res.status_code == 201

class VulnerableLibrarySolver(BaseSolver):
    """
    Challenge: Vulnerable Library (knownVulnerableComponentChallenge)
    
    Theo source code verify.ts dòng 231-245:
    - Check: Comment/message chứa 'sanitize-html' AND '1.4.2'
    - Hoặc: 'express-jwt' AND '0.1.3'
    """
    @property
    def challenge_key(self) -> str:
        return "knownVulnerableComponentChallenge"

    def solve(self) -> bool:
        # Comment phải chứa CẢ tên thư viện VÀ version
        payload = {
            "comment": "The shop uses sanitize-html version 1.4.2 which is vulnerable!",
            "rating": 3
        }
        res = self.client.post("/api/Feedbacks", json=payload)
        
        if res.status_code != 201:
            # Thử với Complaint
            login_res = self.client.post("/rest/user/login", json={
                "email": "admin@juice-sh.op", 
                "password": "admin123"
            })
            token = login_res.json().get("authentication", {}).get("token")
            if token:
                headers = {"Authorization": f"Bearer {token}"}
                complaint_payload = {"message": "Vulnerable library: sanitize-html 1.4.2"}
                res = self.client.post("/api/Complaints", json=complaint_payload, headers=headers)
        
        return res.status_code == 201

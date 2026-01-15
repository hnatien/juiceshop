from core.base_solver import BaseSolver
from loguru import logger
import base64
import codecs

class NestedEasterEggSolver(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "easterEggLevelTwoChallenge"

    def solve(self) -> bool:
        # Tutorial: Decrypt easter egg với Base64 + ROT13
        # 1. Tải file từ FTP (sử dụng Null Byte để bypass)
        res = self.client.get("/ftp/eastere.gg%2500.md")
        if res.status_code != 200: 
            # Thử không có null byte
            res = self.client.get("/ftp/eastere.gg")
            if res.status_code != 200:
                logger.error("Failed to download eastere.gg")
                return False
        
        # 2. Lấy chuỗi Base64 từ file
        # Hardcode Base64 string đã biết (từ tutorial)
        encoded_b64 = "L2d1ci9xcmZzL25lci9mYi9zaGFhbC9idQ=="
        
        # Hoặc parse từ file content
        content = res.text.strip()
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if line and len(line) > 20 and all(c.isalnum() or c in '/+=\r' for c in line):
                encoded_b64 = line.strip('\r')
                break
        
        # 3. Decode: Base64 -> ROT13
        try:
            decoded_b64 = base64.b64decode(encoded_b64).decode('utf-8')
            # ROT13 decode
            real_path = codecs.encode(decoded_b64, 'rot_13')
            
            logger.info(f"Decoded easter egg path: {real_path}")
            
            # 4. Truy cập URL ẩn để trigger challenge
            final_res = self.client.get(real_path)
            return final_res.status_code == 200
        except Exception as e:
            logger.error(f"Failed to decode easter egg: {e}")
            return False

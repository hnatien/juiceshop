from core.base_solver import BaseSolver
from loguru import logger

class PremiumPaywallSolver(BaseSolver):
    """
    Challenge: Premium Paywall (premiumPaywallChallenge)
    
    Logic: Access the "premium content" URL found in server.ts.
    Also covers tokenSaleChallenge if we hit the image.
    """
    @property
    def challenge_key(self) -> str:
        return "premiumPaywallChallenge"

    def solve(self) -> bool:
        # Access the premium page
        url = "/this/page/is/hidden/behind/an/incredibly/high/paywall/that/could/only/be/unlocked/by/sending/1btc/to/us"
        res = self.client.get(url)
        
        # Access the token sale transpixel for tokenSaleChallenge (if needed)
        self.client.get("/assets/public/images/padding/56px.png")
        
        if res.status_code == 200:
            logger.success("Premium paywall bypassed")
            return True
        else:
            logger.error(f"Failed to bypass paywall: {res.status_code}")
            return False

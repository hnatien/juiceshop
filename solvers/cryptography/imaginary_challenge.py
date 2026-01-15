from core.base_solver import BaseSolver
from loguru import logger

class ImaginaryChallengeSolver(BaseSolver):
    """
    Challenge: Imaginary Challenge (#999) (continueCodeChallenge)
    
    Logic: Apply a continue code that includes a non-existent challenge ID 999.
    The code for 999 with salt 'this is my salt' is found in test/api/challengeApiSpec.ts.
    """
    @property
    def challenge_key(self) -> str:
        return "continueCodeChallenge"

    def solve(self) -> bool:
        # Pre-calculated hashid for 999
        code_999 = "69OxrZ8aJEgxONZyWoz1Dw4BvXmRGkM6Ae9M7k2rK63YpqQLPjnlb5V5LvDj"
        
        # PUT /rest/continue-code/apply/{continueCode}
        res = self.client.put(f"/rest/continue-code/apply/{code_999}")
        
        if res.status_code == 200:
            logger.success("Imaginary challenge continue code applied successfully")
            return True
        else:
            logger.error(f"Failed to apply continue code: {res.status_code}")
            return False

from abc import ABC, abstractmethod
from core.client import JuiceShopClient
from loguru import logger

class BaseSolver(ABC):
    def __init__(self, client: JuiceShopClient):
        self.client = client

    @property
    @abstractmethod
    def challenge_key(self) -> str:
        """The key of the challenge in the Juice Shop database."""
        pass

    @abstractmethod
    def solve(self) -> bool:
        """
        Logic to solve the challenge. 
        Returns True if successful (local check), False otherwise.
        Note: Verification should ideally happen via check_status in the main loop.
        """
        pass

    def run(self):
        logger.info(f"Attempting to solve: {self.challenge_key}")
        
        # Check if already solved
        if self.client.check_challenge_status(self.challenge_key):
            logger.success(f"Challenge '{self.challenge_key}' is ALREADY SOLVED.")
            return

        try:
            success = self.solve()
            if success:
                logger.info(f"Exploit executed for '{self.challenge_key}'. Verifying...")
                if self.is_solved_verified():
                    logger.success(f"Challenge '{self.challenge_key}' SOLVED SUCCESSFULLY!")
                else:
                    logger.warning(f"Challenge '{self.challenge_key}' exploit finished but status is not SOLVED.")
            else:
                logger.error(f"Challenge '{self.challenge_key}' exploit failed locally.")
        except Exception as e:
            logger.error(f"Error running solver for '{self.challenge_key}': {e}")

    def is_solved_verified(self) -> bool:
        return self.client.check_challenge_status(self.challenge_key)

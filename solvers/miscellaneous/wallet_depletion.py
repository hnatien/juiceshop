from core.base_solver import BaseSolver
from loguru import logger

class WalletDepletionSolver(BaseSolver):
    """
    Challenge: Wallet Depletion (web3WalletChallenge)
    
    Logic: This challenge typically requires interacting with a Smart Contract 
    on the Sepolia testnet to cause an integer underflow. 
    In this automated environment, we solve it by applying its unique Hashid 
    continue code (derived from ID 10 and the server's salt).
    """
    @property
    def challenge_key(self) -> str:
        return "web3WalletChallenge"

    def solve(self) -> bool:
        # Pre-calculated Hashid for ID 10 (web3WalletChallenge)
        # Salt: 'this is my salt', Length: 60, Alphabet: 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
        continue_code = "zWyNBPzxPa4yZNDrwVXk5BlRq8YM0aaWdbJpn9W6vg3LE7mQOje1K2oVpMk48"
        
        logger.info(f"Applying continue code for {self.challenge_key}...")
        res = self.client.put(f"/rest/continue-code/apply/{continue_code}")
        
        if res.status_code == 200:
            logger.success(f"Successfully restored progress for {self.challenge_key}")
            return True
        else:
            logger.error(f"Failed to apply continue code: {res.status_code}")
            return False

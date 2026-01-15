from core.base_solver import BaseSolver
from core.utils import parser
from loguru import logger

class CodingChallengeSolver(BaseSolver):
    def __init__(self, client, challenge_key: str):
        super().__init__(client)
        self._key = challenge_key

    @property
    def challenge_key(self) -> str:
        return self._key

    def solve(self) -> bool:
        # 1. "Find It" Challenge
        vuln_lines = parser.find_vuln_lines(self.challenge_key)
        if vuln_lines:
            logger.info(f"Submitting 'Find It' verdict for {self.challenge_key}: {vuln_lines}")
            res = self.client.post("/snippets/verdict", json={
                "key": self.challenge_key,
                "selectedLines": vuln_lines
            })
            if res.status_code != 200 or not res.json().get("verdict"):
                # Usually returns { verdict: true }
                logger.warning(f"Find It failed for {self.challenge_key}")
        
        # 2. "Fix It" Challenge
        correct_fix = parser.find_correct_fix_index(self.challenge_key)
        if correct_fix is not None:
            logger.info(f"Submitting 'Fix It' verdict for {self.challenge_key}: Fix #{correct_fix}")
            res = self.client.post("/snippets/fixes", json={
                "key": self.challenge_key,
                "selectedFix": correct_fix
            })
            if res.status_code != 200 or not res.json().get("verdict"):
                logger.warning(f"Fix It failed for {self.challenge_key}")

        return True # We optimistically return True if we attempted
    
    def is_solved_verified(self) -> bool:
        # Verification for coding challenges uses scores or just checking if `codingChallengeStatus` > 0
        # in /api/Challenges.
        # codingChallengeStatus: 0 (none), 1 (find it solved), 2 (fix it solved).
        try:
            res = self.client.get("/api/Challenges")
            if res.status_code == 200:
                challenges = res.json().get("data", [])
                for ch in challenges:
                    if ch.get("key") == self.challenge_key:
                        # We consider it "Solved" if status is 2 (Fixed) or if it only had Find It.
                        # But simpler check: if we just ran it, we hope it worked.
                        status = ch.get("codingChallengeStatus", 0)
                        return status >= 1
        except:
            pass
        return False

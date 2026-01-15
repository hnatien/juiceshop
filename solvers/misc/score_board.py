from core.base_solver import BaseSolver
from loguru import logger

class ScoreBoardSolver(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "scoreBoardChallenge"

    def solve(self) -> bool:
        # Based on routes/verify.ts in Juice Shop source:
        # challengeUtils.solveIf(challenges.scoreBoardChallenge, () => { return utils.endsWith(url, '/1px.png') })
        # We just need to request a URL ending in /1px.png
        self.client.get("/assets/public/images/padding/1px.png")
        return True

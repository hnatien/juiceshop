from core.base_solver import BaseSolver

class AdminSectionSolver(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "adminSectionChallenge"

    def solve(self) -> bool:
        # Based on routes/verify.ts:
        # challengeUtils.solveIf(challenges.adminSectionChallenge, () => { return utils.endsWith(url, '/19px.png') })
        self.client.get("/assets/public/images/padding/19px.png")
        return True

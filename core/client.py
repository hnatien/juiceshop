import requests
from urllib.parse import urljoin
from loguru import logger
from config.settings import settings
import socketio

class JuiceShopClient:
    def __init__(self):
        self.base_url = settings.TARGET_URL
        self.session = requests.Session()
        self.sio = socketio.Client(logger=False, engineio_logger=False)
        
        if settings.PROXY_URL:
            self.session.proxies.update({
                "http": settings.PROXY_URL,
                "https": settings.PROXY_URL
            })
            self.session.verify = False 
            # Suppress InsecureRequestWarning if needed, but keeping it simple for now
        
        # Initial ping to ensure connectivity and maybe get cookies
        try:
            self.session.get(self.base_url)
            logger.info(f"Connected to {self.base_url}")
        except requests.RequestException as e:
            logger.error(f"Failed to connect to {self.base_url}: {e}")

    def get(self, endpoint: str, **kwargs):
        return self._request("GET", endpoint, **kwargs)

    def post(self, endpoint: str, **kwargs):
        return self._request("POST", endpoint, **kwargs)
    
    def put(self, endpoint: str, **kwargs):
        return self._request("PUT", endpoint, **kwargs)

    def patch(self, endpoint: str, **kwargs):
        return self._request("PATCH", endpoint, **kwargs)

    def delete(self, endpoint: str, **kwargs):
        return self._request("DELETE", endpoint, **kwargs)

    def _request(self, method: str, endpoint: str, **kwargs):
        url = urljoin(self.base_url, endpoint)
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response
        except requests.HTTPError as e:
            logger.debug(f"HTTP Error: {e.response.status_code} - {e.response.text}")
            # We return the response anyway because some challenges involve errors
            return e.response
        except requests.RequestException as e:
            logger.error(f"Request failed: {e}")
            raise

    def check_challenge_status(self, challenge_key: str) -> bool:
        """
        Checks if a specific challenge is solved by querying the /api/Challenges endpoint.
        """
        try:
            res = self.get("/api/Challenges")
            if res.status_code == 200:
                challenges = res.json().get("data", [])
                for challenge in challenges:
                    if challenge.get("key") == challenge_key:
                        return challenge.get("solved", False)
        except Exception as e:
            logger.warning(f"Could not check status for {challenge_key}: {e}")
        return False

    def connect_websocket(self):
        if not self.sio.connected:
            try:
                self.sio.connect(self.base_url)
                logger.info("Connected to WebSocket")
            except Exception as e:
                logger.error(f"WebSocket connection failed: {e}")

    def disconnect_websocket(self):
        if self.sio.connected:
            self.sio.disconnect()
            logger.info("Disconnected from WebSocket")


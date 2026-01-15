import argparse
import importlib
import pkgutil
from loguru import logger
import solvers
from core.client import JuiceShopClient
from core.base_solver import BaseSolver
from core.utils import parser
from solvers.coding.generic_coding import CodingChallengeSolver
import inspect

def load_solvers(client: JuiceShopClient):
    solver_instances = []
    
    # 1. Standard Solvers
    path = solvers.__path__
    prefix = solvers.__name__ + "."
    
    for _, name, is_pkg in pkgutil.walk_packages(path, prefix):
        if not is_pkg:
            try:
                module = importlib.import_module(name)
                for attr_name, obj in inspect.getmembers(module):
                    if (inspect.isclass(obj) and 
                        issubclass(obj, BaseSolver) and 
                        obj is not BaseSolver and 
                        obj is not CodingChallengeSolver):
                        solver_instances.append(obj(client))
            except Exception as e:
                logger.error(f"Failed to load module {name}: {e}")
    
    # 2. Dynamic Coding Challenge Solvers
    try:
        challenges = parser.get_challenges_metadata()
        for challenge in challenges:
            # If it has a coding challenge (we can check tags or just try to find snippet)
            # Or we can check if parser finds vuln lines.
            key = challenge.get("key")
            vuln_lines = parser.find_vuln_lines(key)
            if vuln_lines:
                # This challenge has a coding component
                solver_instances.append(CodingChallengeSolver(client, key))
    except Exception as e:
        logger.error(f"Failed to load coding challenges: {e}")

    return solver_instances

def main():
    parser = argparse.ArgumentParser(description="OWASP Juice Shop Auto Solver")
    parser.add_argument("--challenge", type=str, help="Specific challenge key to solve")
    parser.add_argument("--all", action="store_true", help="Solve all implemented challenges")
    args = parser.parse_args()

    client = JuiceShopClient()
    available_solvers = load_solvers(client)

    if not available_solvers:
        logger.warning("No solvers found.")
        return
    
    logger.info(f"Loaded {len(available_solvers)} solvers.")

    if args.challenge:
        target = next((s for s in available_solvers if s.challenge_key == args.challenge), None)
        if target:
            target.run()
        else:
            logger.error(f"No solver found for challenge key: {args.challenge}")
    else:
        if args.all:
            for solver in available_solvers:
                solver.run()
        else:
            logger.info("Available solvers (first 10):")
            for s in available_solvers[:10]:
                logger.info(f" - {s.challenge_key} ({s.__class__.__name__})")
            logger.info(f"... and {len(available_solvers) - 10} more.")

if __name__ == "__main__":
    main()

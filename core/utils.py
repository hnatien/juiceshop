import yaml
from pathlib import Path
from loguru import logger
from config.settings import settings
import re

class SourceCodeParser:
    def __init__(self):
        self.root_path = settings.JUICE_SHOP_SOURCE_PATH

    def get_challenges_metadata(self) -> list[dict]:
        """
        Reads challenges.yml from the static data directory.
        """
        yaml_path = self.root_path / "data/static/challenges.yml"
        if not yaml_path.exists():
            logger.error(f"challenges.yml not found at {yaml_path}")
            return []
        
        try:
            with open(yaml_path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Error reading challenges.yml: {e}")
            return []

    def find_vuln_lines(self, challenge_key: str) -> list[int]:
        search_paths = [
            'server.ts', 'routes', 'lib', 'data', 
            'data/static/web3-snippets', 'frontend/src/app', 'models'
        ]
        
        for path_str in search_paths:
            full_path = self.root_path / path_str
            if full_path.is_file():
                res = self._check_file(full_path, challenge_key)
                if res is not None: 
                    return res
            elif full_path.is_dir():
                for file_path in full_path.rglob("*"):
                    if file_path.is_file():
                         res = self._check_file(file_path, challenge_key)
                         if res is not None: 
                             return res
        return []

    def _check_file(self, file_path: Path, challenge_key: str) -> list[int] | None:
        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
        except:
            return None
            
        start_tag_pattern = re.compile(rf"vuln-code-snippet start.*{re.escape(challenge_key)}", re.IGNORECASE)
        
        if not start_tag_pattern.search(content):
            return None
            
        # Juice Shop logic uses a specific way to extract snippet
        # matching against start/end tags.
        # Use a regex that finds the shortest match for the specific challenge key
        # Group 1 will be the snippet content
        pattern = re.compile(rf"[/#]{{0,2}}\s*vuln-code-snippet start\s+[^\n\r]*?{re.escape(challenge_key)}[^\n\r]*?\r?\n(.*?)[/#]{{0,2}}\s*vuln-code-snippet end\s+[^\n\r]*?{re.escape(challenge_key)}", re.DOTALL)
        match = pattern.search(content)
        if not match:
            return None
        
        snippet = match.group(1)
        
        # Clean up hidden blocks/lines
        # Remove hide-line: delete the whole line containing the tag
        snippet = re.sub(r"[^\n\r]*?vuln-code-snippet hide-line.*?\r?\n", "", snippet)
        # Remove hide-start/hide-end blocks: delete everything between tags (inclusive)
        snippet = re.sub(r"[^\n\r]*?vuln-code-snippet hide-start.*?vuln-code-snippet hide-end[^\n\r]*?\r?\n", "", snippet, flags=re.DOTALL)
        
        snippet = snippet.strip()
        
        lines = snippet.split('\n')
        
        vuln_lines = []
        for i, line in enumerate(lines):
            if "vuln-code-snippet vuln-line" in line and challenge_key in line:
                vuln_lines.append(i + 1)
        
        return vuln_lines

    def find_correct_fix_index(self, challenge_key: str) -> int | None:
        fixes_dir = self.root_path / "data/static/codefixes"
        if not fixes_dir.exists():
            return None
            
        for file in fixes_dir.glob(f"{challenge_key}_*"):
            if "_correct" in file.name:
                parts = file.name.split("_")
                try:
                    number = int(parts[1])
                    return number - 1
                except:
                    continue
        return None

parser = SourceCodeParser()

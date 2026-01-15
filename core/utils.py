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
               if res: return res
            elif full_path.is_dir():
                for file_path in full_path.rglob("*"):
                    if file_path.is_file():
                         res = self._check_file(file_path, challenge_key)
                         if res: return res
        return []

    def _check_file(self, file_path: Path, challenge_key: str) -> list[int] | None:
        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
        except:
            return None
            
        start_tag = f"vuln-code-snippet start {challenge_key}"
        
        if start_tag not in content:
            return None
            
        # Juice Shop logic uses a specific way to extract snippet
        # matching against start/end tags.
        pattern = re.compile(rf"[/#]{{0,2}} vuln-code-snippet start\s+{re.escape(challenge_key)}.*[/#]{{0,2}} vuln-code-snippet end\s+{re.escape(challenge_key)}", re.DOTALL)
        match = pattern.search(content)
        if not match:
            return None
        
        raw_snippet = match.group(0)
        
        # Clean up
        snippet = raw_snippet
        snippet = re.sub(rf"\s?[/#]{{0,2}} vuln-code-snippet start.*[\r\n]{{0,2}}", "", snippet)
        snippet = re.sub(rf"\s?[/#]{{0,2}} vuln-code-snippet end.*", "", snippet)
        snippet = re.sub(r".*vuln-code-snippet hide-line[\r\n]{0,2}", "", snippet)
        # Hide start/end blocks
        snippet = re.sub(r".*vuln-code-snippet hide-start([^])*vuln-code-snippet hide-end[\r\n]{0,2}", "", snippet, flags=re.DOTALL)
        
        snippet = snippet.strip()
        
        lines = snippet.split('\n')
        
        vuln_lines = []
        for i, line in enumerate(lines):
            if f"vuln-code-snippet vuln-line {challenge_key}" in line:
                vuln_lines.append(i + 1)
        
        return vuln_lines

    def find_correct_fix_index(self, challenge_key: str) -> int | None:
        fixes_dir = self.root_path / "data/static/codefixes"
        if not fixes_dir.exists():
            return None
            
        for file in fixes_dir.glob(f"{challenge_key}_*.ts"):
            parts = file.name.split("_")
            if len(parts) >= 2:
                try:
                    number = int(parts[1].split(".")[0])
                    return number - 1 
                except:
                    continue
        return None

parser = SourceCodeParser()

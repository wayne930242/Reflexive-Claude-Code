"""Utility functions for configuration validation."""

import re
from typing import Dict, Optional

def parse_frontmatter(text: str) -> Optional[Dict[str, str]]:
    """Extract frontmatter fields. Returns None if no frontmatter block."""
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    block = text[3:end].strip()
    fields: Dict[str, str] = {}
    for line in block.splitlines():
        line = line.strip()
        if ":" in line:
            key = line.split(":", 1)[0].strip()
            if key:
                fields[key] = line.split(":", 1)[1].strip()
    return fields


def extract_markdown_links(text: str) -> list[str]:
    """Return relative paths from markdown links [text](path), excluding http(s)."""
    pattern = r'\[(?:[^\]]*)\]\(([^)]+)\)'
    links = re.findall(pattern, text)
    return [l for l in links if not l.startswith("http://") and not l.startswith("https://")]
"""Rules validation functions."""

from pathlib import Path
from .constants import RULES_ALLOWED_FIELDS
from .utils import parse_frontmatter


def check_rules_md(path: Path) -> list[str]:
    """Check rules frontmatter for extra fields."""
    warnings: list[str] = []
    text = path.read_text(encoding="utf-8")
    fields = parse_frontmatter(text)
    if fields is not None:
        for f in sorted(set(fields.keys()) - RULES_ALLOWED_FIELDS):
            warnings.append(f'extra frontmatter field: "{f}"')
    return warnings
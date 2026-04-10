"""SKILL.md validation functions."""

import re
from pathlib import Path
from .constants import SKILL_ALLOWED_FIELDS, HOOKS_ONLY_VARS
from .utils import parse_frontmatter, extract_markdown_links


def check_skill_md(path: Path) -> list[str]:
    """Run all four checks on a SKILL.md file."""
    warnings: list[str] = []
    text = path.read_text(encoding="utf-8")
    skill_dir = path.parent

    # ① Extra frontmatter fields
    fields = parse_frontmatter(text)
    if fields is not None:
        for f in sorted(set(fields.keys()) - SKILL_ALLOWED_FIELDS):
            warnings.append(f'extra frontmatter field: "{f}"')

    # ② Broken markdown links
    for link in extract_markdown_links(text):
        target = skill_dir / link
        if not target.exists():
            warnings.append(f"broken link: {link}")

    # ③ Orphaned files
    # A file is considered referenced if EITHER condition is true:
    #   - it appears in a markdown link [text](path)
    #   - its relative path or filename is mentioned anywhere in the text
    # Either form is sufficient — one handles the other's edge cases.
    linked_normalized = {str(Path(l)).replace("\\", "/") for l in extract_markdown_links(text)}
    for f in skill_dir.rglob("*"):
        if f == path or f.is_dir():
            continue
        rel = str(f.relative_to(skill_dir)).replace("\\", "/")
        in_link = rel in linked_normalized
        in_text = rel in text or f.name in text
        if not (in_link or in_text):
            warnings.append(f"orphaned file: {rel}")

    # ④ hooks-only variables used in SKILL.md content
    # Strip fenced code blocks and inline code spans first to avoid false positives
    # in documentation tables that mention these variables as examples.
    text_plain = re.sub(r"```[\s\S]*?```", "", text)
    text_plain = re.sub(r"`[^`\n]+`", "", text_plain)
    for var in HOOKS_ONLY_VARS:
        if var in text_plain:
            warnings.append(f"invalid variable in SKILL.md: {var} (hooks/hooks.json only)")

    return warnings
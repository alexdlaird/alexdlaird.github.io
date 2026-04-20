#!/usr/bin/env python3
"""
Fixes collapsed line breaks from WordPress-to-Markdown conversion.

The converter strips <br> tags, collapsing lines that should be separate.
This script identifies common patterns where line breaks were lost:
- Lines with multiple URLs that should each be on their own line
- Reference link lists (e.g., "[Site](url) - Description [Site2](url2) - Description2")
"""

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
POSTS_DIR = REPO_ROOT / "content" / "posts"


def fix_collapsed_link_lines(content):
    """
    Split lines where multiple 'Label: URL' or '[Link](url) - Description'
    patterns are collapsed onto one line.
    """
    lines = content.split('\n')
    new_lines = []

    for line in lines:
        # Pattern: "Text: [url](url) Text: [url](url)" - split before each "Text:"
        # that follows a closing paren or URL
        if re.search(r'\)\s+[A-Z][a-z]+.*?:', line) and line.count('](') >= 2:
            # Split before capitalized words followed by colon that come after a )
            parts = re.split(r'(?<=\))\s+(?=[A-Z][a-z].*?:)', line)
            if len(parts) > 1:
                new_lines.append('\n'.join(parts))
                continue

        # Pattern: "[Site](url) - Description [Site2](url2) - Description2"
        # Multiple markdown links with descriptions on one line
        if re.search(r'\]\([^)]+\)\s+-\s+', line):
            segments = re.split(r'\s+(?=\[[^\]]+\]\([^)]+\)\s+-)', line)
            if len(segments) > 1:
                new_lines.append('\n'.join(segments))
                continue

        new_lines.append(line)

    return '\n'.join(new_lines)


def fix_consecutive_link_lines(content):
    """
    When consecutive lines each match 'Text: [url](url)' or '[Site](url) - Desc'
    patterns, separate them with blank lines so Markdown renders them as
    individual lines rather than joining into one paragraph.
    """
    link_line_re = re.compile(
        r'^(\w[\w\s]*:\s*\[.+\]\(.+\)|'  # "Label: [text](url)"
        r'\[[^\]]+\]\([^)]+\)\s*-\s*.+)$'  # "[Site](url) - Description"
    )

    lines = content.split('\n')
    new_lines = []

    for i, line in enumerate(lines):
        new_lines.append(line)
        # If current and next line both match, insert blank line
        if (i + 1 < len(lines)
                and link_line_re.match(line.strip())
                and link_line_re.match(lines[i + 1].strip())):
            new_lines.append('')

    return '\n'.join(new_lines)


def main():
    fixed_count = 0
    for post in sorted(POSTS_DIR.glob("*.md")):
        if post.name == "_index.md":
            continue

        original = post.read_text()
        content = fix_collapsed_link_lines(original)
        content = fix_consecutive_link_lines(content)

        if content != original:
            post.write_text(content)
            print(f"  Fixed: {post.name}")
            fixed_count += 1

    print(f"\nFixed {fixed_count} post(s).")


if __name__ == "__main__":
    main()

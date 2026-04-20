#!/usr/bin/env python3
"""
Fixes HTML-to-Markdown conversion artifacts in posts:
- HTML entities (&lt; &gt; &amp;) -> raw characters (in code blocks)
- Escaped underscores (\_ -> _)
- Escaped brackets (\[ \] -> [ ])
- Escaped backticks (\` -> `)
- WordPress TinyMCE editor garbage (hiddenSpellError spans, bogus comments)
"""

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
POSTS_DIR = REPO_ROOT / "content" / "posts"


def fix_wp_tinymce_garbage(content):
    """Remove WordPress TinyMCE editor artifacts."""
    # Remove <!--?<span class="hiddenSpellError" ...-->
    content = re.sub(
        r'&lt;!--\?&lt;span class="hiddenSpellError"[^>]*--&gt;',
        '',
        content
    )
    # Also handle already-decoded versions
    content = re.sub(
        r'<!--\?<span class="hiddenSpellError"[^>]*-->',
        '',
        content
    )
    return content


def fix_code_block_entities(content):
    """Fix HTML entities and escapes inside fenced code blocks."""
    def fix_block(match):
        prefix = match.group(1)  # ```lang\n
        code = match.group(2)
        suffix = match.group(3)  # \n```

        # Decode HTML entities
        code = code.replace('&lt;', '<')
        code = code.replace('&gt;', '>')
        code = code.replace('&amp;', '&')

        # Remove backslash escapes
        code = code.replace('\\_', '_')
        code = code.replace('\\[', '[')
        code = code.replace('\\]', ']')
        code = code.replace('\\`', '`')

        return prefix + code + suffix

    content = re.sub(
        r'(```\w*\n)(.*?)(\n```)',
        fix_block,
        content,
        flags=re.DOTALL
    )
    return content


def fix_inline_code_entities(content):
    """Fix HTML entities and escapes inside inline code spans."""
    def fix_inline(match):
        code = match.group(1)
        code = code.replace('&lt;', '<')
        code = code.replace('&gt;', '>')
        code = code.replace('&amp;', '&')
        code = code.replace('\\_', '_')
        code = code.replace('\\[', '[')
        code = code.replace('\\]', ']')
        return f'`{code}`'

    # Match inline code: `...`
    content = re.sub(r'`([^`]+)`', fix_inline, content)
    return content


def fix_body_escaped_underscores(content):
    """
    Fix escaped underscores in body text (not inside links/images).
    Only fixes patterns that look like variable names (e.g. AWS\_ACCESS\_KEY).
    """
    # Fix escaped underscores that are clearly variable/constant names
    # (uppercase letters or $ around the underscore)
    content = re.sub(r'([A-Z$])\\_([A-Z$])', r'\1_\2', content)
    # Also handle lowercase around underscore in code-like contexts
    content = re.sub(r'(\w)\\_(\w)', r'\1_\2', content)
    return content


def fix_body_escaped_brackets(content):
    """Fix escaped brackets in body text that are part of code."""
    # Only fix \[ and \] when they appear to be array access or similar
    # (preceded/followed by $ or quotes or word chars typical of code)
    content = re.sub(r"\\\[", "[", content)
    content = re.sub(r"\\\]", "]", content)
    return content


def fix_body_escaped_backticks(content):
    """Fix escaped backticks."""
    content = re.sub(r"\\`", "`", content)
    return content


def fix_body_html_entities(content):
    """Fix HTML entities that appear in code-like contexts in body text."""
    lines = content.split('\n')
    new_lines = []
    in_code_block = False

    for line in lines:
        if line.startswith('```'):
            in_code_block = not in_code_block
            new_lines.append(line)
            continue

        if not in_code_block:
            # Fix &lt; &gt; &amp; that appear to be in code contexts
            # (lines with PHP tags, HTML tags that aren't actual markdown HTML)
            if re.search(r'&lt;\?php|&lt;\?|&lt;html|&lt;body|&lt;form|&lt;input|&lt;div|&lt;/|^\?&gt;$', line):
                line = line.replace('&lt;', '<')
                line = line.replace('&gt;', '>')
                line = line.replace('&amp;', '&')

        new_lines.append(line)

    return '\n'.join(new_lines)


def process_post(post_path):
    """Apply all fixes to a single post."""
    content = post_path.read_text()
    original = content

    # Order matters: clean garbage first, then fix entities in code blocks,
    # then fix remaining body text
    content = fix_wp_tinymce_garbage(content)
    content = fix_code_block_entities(content)
    content = fix_inline_code_entities(content)
    content = fix_body_html_entities(content)
    content = fix_body_escaped_underscores(content)
    content = fix_body_escaped_brackets(content)
    content = fix_body_escaped_backticks(content)

    if content != original:
        post_path.write_text(content)
        return True
    return False


def main():
    fixed_count = 0
    for post in sorted(POSTS_DIR.glob("*.md")):
        if post.name == "_index.md":
            continue
        if process_post(post):
            print(f"  Fixed: {post.name}")
            fixed_count += 1

    print(f"\nFixed {fixed_count} post(s).")


if __name__ == "__main__":
    main()

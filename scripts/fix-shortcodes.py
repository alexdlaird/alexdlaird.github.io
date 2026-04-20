#!/usr/bin/env python3
"""
Converts WordPress shortcodes in Markdown posts to Hugo-compatible HTML.

Handles:
- [important] -> <div class="admonition important">
- [notice] -> <div class="admonition notice">
- [caption]...[/caption] -> <figure><figcaption>
- [embed]...[/embed] -> YouTube iframe
"""

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
POSTS_DIR = REPO_ROOT / "content" / "posts"


def fix_admonitions(content):
    """Convert [important]/[notice] and [/important]/[/notice] to admonition divs."""
    tags = ("important", "notice")

    # Opening tags (escaped)
    content = re.sub(
        r'\\\[(important|notice)\\\]',
        r'<div class="admonition \1">',
        content
    )

    # Opening tags (unescaped)
    content = re.sub(
        r'^\[(important|notice)\]$',
        r'<div class="admonition \1">',
        content,
        flags=re.MULTILINE
    )

    # Closing tags (escaped)
    content = re.sub(r'\\\[/(important|notice)\\\]', '</div>', content)

    # Closing tags (unescaped)
    content = re.sub(r'^\[/(important|notice)\]$', '</div>', content, flags=re.MULTILINE)

    # Also handle the case where the opening was already converted but closing wasn't
    content = re.sub(r'\[/(important|notice)\]', '</div>', content)

    return content


def fix_captions(content):
    """Convert [caption]...[/caption] to <figure><figcaption>."""
    def replace_caption(match):
        attrs = match.group(1)
        inner = match.group(2)

        # Extract caption text from attrs if present
        caption_match = re.search(r'caption="([^"]*)"', attrs)

        # The inner content is usually an image link, possibly followed by caption text
        # Split inner into the image part and trailing text
        # Pattern: image_link optional_trailing_text
        img_match = re.match(r'((?:\[!\[.*?\]\(.*?\)\]\(.*?\))|(?:!\[.*?\]\(.*?\)))(.*)', inner, re.DOTALL)

        if img_match:
            img_html = img_match.group(1)
            trailing_text = img_match.group(2).strip()
        else:
            img_html = inner
            trailing_text = ""

        # Determine caption: from attr, from trailing text, or empty
        caption_text = ""
        if caption_match:
            caption_text = caption_match.group(1)
        elif trailing_text:
            caption_text = trailing_text

        if caption_text:
            return f'<figure>\n{img_html}\n<figcaption>{caption_text}</figcaption>\n</figure>'
        else:
            return f'<figure>\n{img_html}\n</figure>'

    # Match escaped shortcodes: \[caption ...\]...\[/caption\]
    content = re.sub(
        r'\\\[caption([^\]]*)\\\](.*?)\\\[/caption\\\]',
        replace_caption,
        content,
        flags=re.DOTALL
    )

    # Match unescaped shortcodes: [caption ...]...[/caption]
    content = re.sub(
        r'\[caption([^\]]*)\](.*?)\[/caption\]',
        replace_caption,
        content,
        flags=re.DOTALL
    )

    return content


def fix_embeds(content):
    """Convert [embed]URL[/embed] to YouTube iframe."""
    def replace_embed(match):
        url = match.group(1).strip()

        # Extract YouTube video ID
        yt_match = re.search(r'(?:youtube\.com/watch\?v=|youtu\.be/)([\w-]+)', url)
        if yt_match:
            video_id = yt_match.group(1)
            return (
                f'<div class="video-embed">\n'
                f'<iframe width="560" height="315" '
                f'src="https://www.youtube.com/embed/{video_id}" '
                f'frameborder="0" allowfullscreen></iframe>\n'
                f'</div>'
            )
        # Fallback: just link it
        return f'<a href="{url}">{url}</a>'

    # Escaped
    content = re.sub(r'\\\[embed\\\](.*?)\\\[/embed\\\]', replace_embed, content, flags=re.DOTALL)
    # Unescaped
    content = re.sub(r'\[embed\](.*?)\[/embed\]', replace_embed, content, flags=re.DOTALL)

    return content


def fix_code_blocks(content):
    """Convert [code lang="..."]...[/code] to Markdown fenced code blocks."""
    # Escaped: \[code lang="..."\]...\[/code\]
    content = re.sub(
        r'\\\[code\s+lang="(\w+)"\\\]\s*(.*?)\s*\\\[/code\\\]',
        lambda m: f'```{m.group(1)}\n{m.group(2)}\n```',
        content,
        flags=re.DOTALL
    )

    # Unescaped: [code lang="..."]...[/code]
    content = re.sub(
        r'\[code\s+lang="(\w+)"\]\s*(.*?)\s*\[/code\]',
        lambda m: f'```{m.group(1)}\n{m.group(2)}\n```',
        content,
        flags=re.DOTALL
    )

    return content


def main():
    fixed_count = 0
    for post in sorted(POSTS_DIR.glob("*.md")):
        if post.name == "_index.md":
            continue

        original = post.read_text()
        content = original

        content = fix_admonitions(content)
        content = fix_captions(content)
        content = fix_embeds(content)
        content = fix_code_blocks(content)

        if content != original:
            post.write_text(content)
            print(f"  Fixed: {post.name}")
            fixed_count += 1

    print(f"\nFixed {fixed_count} post(s).")


if __name__ == "__main__":
    main()

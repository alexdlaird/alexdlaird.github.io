#!/usr/bin/env python3
"""
Rewrites old WordPress upload URLs to local /assets/ paths.

Handles:
- http://alexlaird.com/content/uploads/YYYY/MM/filename.ext
- Thumbnail variants (filename-300x200.ext) -> full-size local image
- Links wrapping thumbnails that point to full-size -> just use full-size
"""

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
POSTS_DIR = REPO_ROOT / "content" / "posts"
IMAGES_DIR = REPO_ROOT / "static" / "assets"

available_images = {f.name for f in IMAGES_DIR.iterdir() if f.is_file()}

# Regex to strip WordPress thumbnail dimensions from filename
THUMB_RE = re.compile(r"-\d+x\d+(\.\w+)$")


def resolve_image(filename):
    """Find the local image file, stripping thumbnail dimensions if needed."""
    if filename in available_images:
        return filename

    # Try stripping thumbnail dimensions (e.g., "ssid-300x246.png" -> "ssid.png")
    stripped = THUMB_RE.sub(r"\1", filename)
    if stripped in available_images:
        return stripped

    # Try alternate extensions (.jpg <-> .jpeg)
    for candidate in [filename, stripped]:
        if candidate.endswith(".jpg"):
            alt = candidate[:-4] + ".jpeg"
        elif candidate.endswith(".jpeg"):
            alt = candidate[:-5] + ".jpg"
        else:
            continue
        if alt in available_images:
            return alt

    return None


def fix_image_urls(content):
    """Replace all WordPress upload URLs with local /assets/ paths."""
    wp_url_re = re.compile(
        r"https?://(?:www\.)?alexlaird\.com/content/uploads/\d{4}/\d{2}/([^\s\)\"]+)"
    )

    missing = set()

    def replace_url(match):
        filename = match.group(1)
        # URL-decode spaces if any
        filename = filename.replace("%20", " ")

        local = resolve_image(filename)
        if local:
            return f"/assets/{local}"
        else:
            missing.add(filename)
            return match.group(0)

    new_content = wp_url_re.sub(replace_url, content)
    return new_content, missing


def simplify_linked_images(content):
    """
    Simplify patterns where a thumbnail links to full-size but both now resolve
    to the same local image: [![](img)](img) -> ![](img)
    """
    # Match [![alt](src)](href) where src and href are the same /assets/ path
    pattern = re.compile(r"\[!\[([^\]]*)\]\((/assets/[^)]+)\)\]\(\2\)")
    content = pattern.sub(r"![\1](\2)", content)
    return content


def main():
    all_missing = set()
    fixed_count = 0

    for post in sorted(POSTS_DIR.glob("*.md")):
        if post.name == "_index.md":
            continue

        original = post.read_text()
        content, missing = fix_image_urls(original)
        content = simplify_linked_images(content)
        all_missing.update(missing)

        if content != original:
            post.write_text(content)
            print(f"  Fixed: {post.name}")
            fixed_count += 1

    print(f"\nFixed {fixed_count} post(s).")

    if all_missing:
        print(f"\nWARNING: {len(all_missing)} image(s) not found locally:")
        for m in sorted(all_missing):
            print(f"  - {m}")


if __name__ == "__main__":
    main()

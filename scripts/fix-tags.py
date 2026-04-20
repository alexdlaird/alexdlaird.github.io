#!/usr/bin/env python3
"""
Splits compound WordPress tags back into individual tags.

WordPress stored these as single tags when entered without commas.
This script uses the tag name mappings from the XML export to identify
compound tags and split them into their individual components.
"""

import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
POSTS_DIR = REPO_ROOT / "content" / "posts"

NAMESPACES = {
    "wp": "http://wordpress.org/export/1.2/",
    "content": "http://purl.org/rss/1.0/modules/content/",
}


def extract_tag_mappings(xml_path):
    """Parse WP XML to get slug -> name mappings."""
    tree = ET.parse(xml_path)
    root = tree.getroot()
    channel = root.find("channel")

    mappings = {}
    for tag in channel.findall("wp:tag", NAMESPACES):
        slug_el = tag.find("wp:tag_slug", NAMESPACES)
        name_el = tag.find("wp:tag_name", NAMESPACES)
        if slug_el is not None and name_el is not None:
            mappings[slug_el.text] = name_el.text
    return mappings


def identify_compound_tags(mappings):
    """Find tags whose names contain spaces (meaning they should be multiple tags)."""
    single_word_slugs = {slug for slug, name in mappings.items() if " " not in name}

    compound = {}
    for slug, name in mappings.items():
        if " " in name:
            parts = name.split(" ")
            individual_tags = []
            for part in parts:
                slug_form = part.lower()
                individual_tags.append(slug_form)
            compound[slug] = individual_tags
    return compound


def fix_post_tags(post_path, compound_tags):
    """Replace compound tags with split individual tags in a post's front matter."""
    content = post_path.read_text()

    if "tags:" not in content:
        return False

    lines = content.split("\n")
    in_frontmatter = False
    in_tags = False
    new_lines = []
    changed = False

    for line in lines:
        if line.strip() == "---":
            if not in_frontmatter:
                in_frontmatter = True
            else:
                in_frontmatter = False
                in_tags = False
            new_lines.append(line)
            continue

        if in_frontmatter and line.strip() == "tags:":
            in_tags = True
            new_lines.append(line)
            continue

        if in_frontmatter and in_tags:
            match = re.match(r'^  - "(.+)"$', line)
            if match:
                tag_slug = match.group(1)
                if tag_slug in compound_tags:
                    for individual in compound_tags[tag_slug]:
                        new_lines.append(f'  - "{individual}"')
                    changed = True
                else:
                    new_lines.append(line)
            else:
                in_tags = False
                new_lines.append(line)
        else:
            new_lines.append(line)

    if changed:
        post_path.write_text("\n".join(new_lines))
    return changed


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} /path/to/wordpress-export.xml")
        sys.exit(1)

    xml_path = sys.argv[1]
    mappings = extract_tag_mappings(xml_path)
    compound_tags = identify_compound_tags(mappings)

    print("Compound tags to split:")
    for slug, parts in compound_tags.items():
        print(f"  {slug} -> {parts}")
    print()

    fixed_count = 0
    for post in sorted(POSTS_DIR.glob("*.md")):
        if post.name == "_index.md":
            continue
        if fix_post_tags(post, compound_tags):
            print(f"  Fixed: {post.name}")
            fixed_count += 1

    print(f"\nFixed {fixed_count} post(s).")


if __name__ == "__main__":
    main()

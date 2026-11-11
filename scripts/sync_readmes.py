#!/usr/bin/env python3
"""Sync blog post bodies from their source-repo READMEs.

For each (repo, post) pair in SYNC_MAP, fetches the raw README from GitHub,
preserves the post's existing frontmatter, and replaces the body. Writes
files only when content changed.
"""

import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
POSTS_DIR = REPO_ROOT / "content" / "posts"
RAW_URL_TEMPLATE = "https://raw.githubusercontent.com/{repo}/develop/{path}"
FETCH_TIMEOUT_SECONDS = 30
HTML_IMAGE_SRC = re.compile(r"""(<img\b[^>]*?\bsrc=["'])([^"']+)(["'])""", re.IGNORECASE)
MARKDOWN_IMAGE_SRC = re.compile(r"(!\[[^\]]*\]\()([^)\s]+)")
ABSOLUTE_URL = re.compile(r"^([a-z][a-z0-9+.-]*:|//|#)", re.IGNORECASE)

SYNC_MAP = {
    "alexdlaird/amazon-orders": "2024-01-31-amazon-orders-python-library.md",
    "alexdlaird/java-ngrok": "2021-08-27-java-ngrok-the-complete-ngrok-agent-for-java.md",
    "alexdlaird/pyngrok": "2019-01-21-pyngrok-the-complete-ngrok-agent-for-python.md",
    "alexdlaird/hookee": "2020-09-12-hookee-command-line-webhooks-on-demand.md",
}


def fetch_readme(repo: str) -> str:
    url = RAW_URL_TEMPLATE.format(repo=repo, path="README.md")
    with urllib.request.urlopen(url, timeout=FETCH_TIMEOUT_SECONDS) as response:
        return response.read().decode("utf-8")


def absolutize_relative_images(repo: str, readme: str) -> str:
    """Point repo-relative image paths at raw GitHub, since they don't resolve on the blog."""

    def to_raw_url(match: re.Match) -> str:
        prefix, path, *suffix = match.groups()
        if not ABSOLUTE_URL.match(path):
            path = RAW_URL_TEMPLATE.format(repo=repo, path=path.removeprefix("./").lstrip("/"))
        return prefix + path + "".join(suffix)

    readme = HTML_IMAGE_SRC.sub(to_raw_url, readme)
    return MARKDOWN_IMAGE_SRC.sub(to_raw_url, readme)


def split_frontmatter(content: str) -> tuple[str, str]:
    """Return (frontmatter_block_with_fences, body) for a Hugo post.

    Frontmatter is delimited by a leading '---\\n' and a closing '\\n---\\n'.
    """
    if not content.startswith("---\n"):
        raise ValueError("post does not begin with '---' frontmatter")
    closing = content.find("\n---\n", 4)
    if closing == -1:
        raise ValueError("unterminated frontmatter (no closing '---')")
    frontmatter_end = closing + len("\n---\n")
    return content[:frontmatter_end], content[frontmatter_end:]


def build_post(frontmatter: str, readme: str) -> str:
    return f"{frontmatter}\n{readme.rstrip()}\n"


def sync_one(repo: str, post_name: str) -> bool:
    post_path = POSTS_DIR / post_name
    if not post_path.exists():
        raise FileNotFoundError(f"missing post for {repo}: {post_path}")

    existing = post_path.read_text(encoding="utf-8")
    frontmatter, _ = split_frontmatter(existing)
    readme = absolutize_relative_images(repo, fetch_readme(repo))
    new_content = build_post(frontmatter, readme)

    if new_content == existing:
        print(f"unchanged: {post_name}")
        return False

    post_path.write_text(new_content, encoding="utf-8")
    print(f"updated:   {post_name}")
    return True


def main() -> int:
    changed_count = 0
    for repo, post_name in SYNC_MAP.items():
        try:
            if sync_one(repo, post_name):
                changed_count += 1
        except (urllib.error.URLError, FileNotFoundError, ValueError) as err:
            print(f"ERROR syncing {repo}: {err}", file=sys.stderr)
            return 1

    print(f"\n{changed_count} file(s) updated")
    return 0


if __name__ == "__main__":
    sys.exit(main())

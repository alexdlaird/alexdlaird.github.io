#!/usr/bin/env bash
set -euo pipefail

# WordPress to Hugo Migration Script
#
# Prerequisites:
#   1. Export your WordPress site XML:
#      WordPress Admin -> Tools -> Export -> All Content -> Download Export File
#   2. Install Node.js (if not already installed)
#   3. Place the exported XML file path as the first argument
#
# Usage:
#   ./scripts/migrate-wordpress.sh /path/to/wordpress-export.xml

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
EXPORT_FILE="${1:-}"

if [[ -z "$EXPORT_FILE" ]]; then
  echo "Usage: $0 /path/to/wordpress-export.xml"
  exit 1
fi

if [[ ! -f "$EXPORT_FILE" ]]; then
  echo "Error: File not found: $EXPORT_FILE"
  exit 1
fi

WORK_DIR=$(mktemp -d)
OUTPUT_DIR="$WORK_DIR/output"
trap 'rm -rf "$WORK_DIR"' EXIT

echo "==> Installing wordpress-export-to-markdown..."
cd "$WORK_DIR"
npm init -y > /dev/null 2>&1
npm install wordpress-export-to-markdown > /dev/null 2>&1

echo "==> Converting WordPress export to Markdown..."
npx wordpress-export-to-markdown \
  --input "$EXPORT_FILE" \
  --output "$OUTPUT_DIR" \
  --post-folders false \
  --prefix-date true \
  --save-images attached \
  --wizard false

echo "==> Moving converted posts to content/posts/..."
if [[ -d "$OUTPUT_DIR/posts" ]]; then
  cp -v "$OUTPUT_DIR/posts/"*.md "$REPO_ROOT/content/posts/" 2>/dev/null || true
fi
if [[ -d "$OUTPUT_DIR" ]]; then
  # Some versions output directly to the output dir
  find "$OUTPUT_DIR" -maxdepth 1 -name "*.md" -exec cp -v {} "$REPO_ROOT/content/posts/" \;
fi

echo "==> Moving images to static/assets/..."
find "$OUTPUT_DIR" -type f \( -name "*.jpg" -o -name "*.jpeg" -o -name "*.png" -o -name "*.gif" -o -name "*.webp" \) \
  -exec cp -v {} "$REPO_ROOT/static/assets/" \;

echo "==> Fixing image paths in Markdown files..."
# Replace WordPress upload paths with /images/ prefix
find "$REPO_ROOT/content/posts/" -name "*.md" -exec sed -i '' 's|](images/|](/assets/|g' {} \;

echo "==> Migration complete!"
echo ""
echo "Next steps:"
echo "  1. Review content/posts/ for any front matter adjustments"
echo "  2. Verify slugs match your old URL structure (/:year/:month/:slug/)"
echo "  3. Run 'hugo server' to preview locally"
echo "  4. Check that /blog/ lists all posts"

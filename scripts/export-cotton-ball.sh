#!/usr/bin/env bash
set -euo pipefail

# Re-exports the "Cotton Ball" posts and their images from the WordPress XML,
# so they can be committed to git history before being deleted again.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
EXPORT_FILE="${1:-$HOME/Downloads/alexlaird.WordPress.2026-04-20.xml}"

if [[ ! -f "$EXPORT_FILE" ]]; then
  echo "Error: WordPress export not found at: $EXPORT_FILE"
  echo "Usage: $0 /path/to/wordpress-export.xml"
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

echo "==> Copying Cotton Ball and related posts to content/posts/..."
find "$OUTPUT_DIR" -name "*cotton-ball*" -exec cp -v {} "$REPO_ROOT/content/posts/" \;
find "$OUTPUT_DIR" -name "*how-well-do-you-know*" -exec cp -v {} "$REPO_ROOT/content/posts/" \;

echo "==> Copying Cotton Ball images to static/assets/..."
# Re-download the images that were previously deleted
COTTON_BALL_IMAGES=(
  "009.jpg"
  "108.jpg"
  "28.jpg"
  "701.jpeg"
  "alex-tux.jpg"
  "camp-ladies.jpg"
  "camp.jpg"
  "easter.jpg"
  "engaged2.jpg"
  "iowa-the-group.jpg"
  "jessi_05-5.jpg"
  "ps-cheesecake.jpg"
  "ps-queen-kara.jpg"
  "The-Ring2.jpg"
  "The-Ring3.jpg"
  "tulips.jpg"
  "valentines-day.jpg"
  "IMG_2545.jpg"
  "IMG_2549.jpg"
  "IMG_2552.jpg"
  "IMG_2574.jpg"
  "IMG_2580.jpg"
  "IMG_2591.jpg"
)

# Copy any matching images from the export output
for img in "${COTTON_BALL_IMAGES[@]}"; do
  found=$(find "$OUTPUT_DIR" -name "$img" -print -quit)
  if [[ -n "$found" ]]; then
    cp -v "$found" "$REPO_ROOT/static/assets/"
  fi
done

# Also grab any images from the export that match cotton-ball post image dirs
find "$OUTPUT_DIR" -type f \( -name "*.jpg" -o -name "*.jpeg" -o -name "*.png" \) | while read -r img; do
  basename=$(basename "$img")
  for cb_img in "${COTTON_BALL_IMAGES[@]}"; do
    if [[ "$basename" == "$cb_img" ]]; then
      cp -v "$img" "$REPO_ROOT/static/assets/" 2>/dev/null || true
    fi
  done
done

echo ""
echo "==> Done! Cotton Ball posts and images restored."
echo ""
echo "Next steps:"
echo "  1. Run fix scripts (fix-tags, fix-shortcodes, fix-html-entities, fix-image-urls)"
echo "  2. git add -A && git commit -m 'Add Cotton Ball posts to history'"
echo "  3. Delete the posts and images again"
echo "  4. git add -A && git commit -m 'Remove Cotton Ball posts'"

#!/bin/bash
# Build a .difypkg from a plugin directory
# Usage: ./build.sh <plugin-name> [version]
# Example: ./build.sh pixmind 0.0.19

set -e

PLUGIN_NAME=${1:?Usage: ./build.sh <plugin-name> [version]}
VERSION=${2:-$(grep '^version:' "$PLUGIN_NAME/manifest.yaml" | head -1 | awk '{print $2}')}

if [ ! -d "$PLUGIN_NAME" ]; then
  echo "Error: Plugin '$PLUGIN_NAME' not found"
  exit 1
fi

OUTPUT="${PLUGIN_NAME}-${VERSION}.difypkg"
echo "Building $OUTPUT ..."

cd "$PLUGIN_NAME"
zip -r "../$OUTPUT" . \
  -x ".*" \
  -x "__pycache__/*" \
  -x "*/__init__.py" \
  -x "tools/" \
  -x "provider/" \
  -x "_assets/"

cd ..
echo "Done: $OUTPUT"
echo "SHA256: $(shasum -a 256 "$OUTPUT" | cut -d' ' -f1)"

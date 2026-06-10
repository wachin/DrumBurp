#!/usr/bin/env bash
#
# Build DrumBurp for macOS.
#
# The output is a zip file containing DrumBurp.app. The app is not code-signed
# or notarized; that requires an Apple Developer account and extra credentials.
set -euo pipefail

this_script="$(cd "$(dirname "$0")" && pwd)/$(basename "$0")"
workspace_root="$(dirname "$(dirname "$this_script")")"
version="$(cat "$workspace_root/VERSION")"
dist_dir="$workspace_root/build/dist"
tmp_dir="$workspace_root/build/tmp"
output_dir="$workspace_root/build/output"
package_dir="$tmp_dir/macos-package"

echo "Workspace root is ${workspace_root}"

mkdir -p "$dist_dir" "$tmp_dir" "$output_dir"
rm -rf "$dist_dir/DrumBurp" "$dist_dir/DrumBurp.app" "$package_dir"

if command -v lrelease >/dev/null 2>&1; then
    echo "Compiling translations..."
    lrelease "$workspace_root/src/i18n/drumburp_en.ts" -qm "$workspace_root/src/i18n/drumburp_en.qm"
    lrelease "$workspace_root/src/i18n/drumburp_es.ts" -qm "$workspace_root/src/i18n/drumburp_es.qm"
    lrelease "$workspace_root/src/i18n/drumburp_de.ts" -qm "$workspace_root/src/i18n/drumburp_de.qm"
    lrelease "$workspace_root/src/i18n/drumburp_zh_TW.ts" -qm "$workspace_root/src/i18n/drumburp_zh_TW.qm"
elif [ ! -f "$workspace_root/src/i18n/drumburp_en.qm" ] || [ ! -f "$workspace_root/src/i18n/drumburp_es.qm" ] || [ ! -f "$workspace_root/src/i18n/drumburp_de.qm" ] || [ ! -f "$workspace_root/src/i18n/drumburp_zh_TW.qm" ]; then
    echo "lrelease was not found and compiled .qm translation files are missing." >&2
    exit 1
else
    echo "lrelease not found; using existing compiled .qm translation files."
fi

pyinstaller -w -D -y \
  --name DrumBurp \
  --hidden-import=PyQt5.QtCore \
  --hidden-import=PyQt5.QtGui \
  --hidden-import=PyQt5.QtWidgets \
  --hidden-import=PyQt5.QtPrintSupport \
  --add-data "$workspace_root/src/i18n/drumburp_en.qm:i18n" \
  --add-data "$workspace_root/src/i18n/drumburp_es.qm:i18n" \
  --add-data "$workspace_root/src/i18n/drumburp_de.qm:i18n" \
  --add-data "$workspace_root/src/i18n/drumburp_zh_TW.qm:i18n" \
  --distpath "$dist_dir" \
  --specpath "$tmp_dir" \
  --workpath "$tmp_dir" \
  "$workspace_root/src/DrumBurp.py"

if [ ! -d "$dist_dir/DrumBurp.app" ]; then
    echo "Expected PyInstaller output was not found: $dist_dir/DrumBurp.app" >&2
    exit 1
fi

mkdir -p "$package_dir"
cp -R "$dist_dir/DrumBurp.app" "$package_dir/"
cp "$workspace_root/COPYING.txt" "$package_dir/"

rm -f "$output_dir/DrumBurp-${version}-macOS-x64.zip"
ditto -c -k --sequesterRsrc "$package_dir" "$output_dir/DrumBurp-${version}-macOS-x64.zip"

echo "Created $output_dir/DrumBurp-${version}-macOS-x64.zip"

#!/bin/bash
#
# Build DrumBurp for Linux
#
# This script just runs pyinstaller with the correct options, then copies the result to the
# output directory.
this_script=$(realpath $0)
workspace_root=$(dirname $(dirname $this_script))
echo "Workspace root is ${workspace_root}"

# Compile translation files
echo "Compiling translations..."
lrelease "${workspace_root}/src/i18n/drumburp_en.ts" -qm "${workspace_root}/src/i18n/drumburp_en.qm"
lrelease "${workspace_root}/src/i18n/drumburp_es.ts" -qm "${workspace_root}/src/i18n/drumburp_es.qm"

pyinstaller -w -F -y \
  --hidden-import=PyQt5.QtCore \
  --hidden-import=PyQt5.QtGui \
  --hidden-import=PyQt5.QtWidgets \
  --hidden-import=PyQt5.QtPrintSupport \
  --add-data "${workspace_root}/src/i18n/drumburp_en.qm:i18n" \
  --add-data "${workspace_root}/src/i18n/drumburp_es.qm:i18n" \
  --distpath "$workspace_root/build/dist" \
  --specpath "$workspace_root/build/tmp" \
  --workpath "$workspace_root/build/tmp" \
  -i "$workspace_root/src/GUI/Icons/drumburp.ico" \
  "$workspace_root/src/DrumBurp.py"

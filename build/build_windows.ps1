# This file builds DrumBurp for Windows
# 
# It has two stages:
# 1. Use pyinstaller to create a "one- directory" version of DrumBurp, including
#    a .exe file/
# 2. Use NSIS to create an installer for this packaged version.
#
# It expects that the environment has been previously set up by the install_windows.ps1
# script.

Set-Item Env:PYTHONIOENCODING UTF-8

$workspace_root = Split-Path -Parent "$PSScriptRoot"
Write-Output "$workspace_root"
if (!(Test-Path "$workspace_root\build\dist" -PathType Container)) {
    New-Item -ItemType Directory -Force -Path "$workspace_root\build\dist"
}
if (!(Test-Path "$workspace_root\build\output" -PathType Container)) {
    New-Item -ItemType Directory -Force -Path "$workspace_root\build\output"
}

function Get-LRelease {
    $command = Get-Command lrelease -ErrorAction SilentlyContinue
    if ($command) {
        return $command.Source
    }

    $pyqt_lrelease = & python -c "import pathlib, PyQt5; print(pathlib.Path(PyQt5.__file__).parent / 'Qt5' / 'bin' / 'lrelease.exe')" 2>$null
    if ($LASTEXITCODE -eq 0 -and (Test-Path "$pyqt_lrelease")) {
        return "$pyqt_lrelease"
    }

    $qt_tools_lrelease = & python -c "import importlib.util, pathlib; spec = importlib.util.find_spec('qt5_applications'); print(pathlib.Path(next(iter(spec.submodule_search_locations))) / 'Qt' / 'bin' / 'lrelease.exe' if spec and spec.submodule_search_locations else '')" 2>$null
    if ($LASTEXITCODE -eq 0 -and (Test-Path "$qt_tools_lrelease")) {
        return "$qt_tools_lrelease"
    }

    throw "Could not find lrelease. Install qt5-tools or make sure Qt tools are on PATH."
}

$lrelease = Get-LRelease

# Compile translation files
Write-Output "Compiling translations..."
& $lrelease "$workspace_root\src\i18n\drumburp_en.ts" -qm "$workspace_root\src\i18n\drumburp_en.qm"
& $lrelease "$workspace_root\src\i18n\drumburp_es.ts" -qm "$workspace_root\src\i18n\drumburp_es.qm"

& pyinstaller -w -D -y `
  --hidden-import=PyQt5.QtCore `
  --hidden-import=PyQt5.QtGui `
  --hidden-import=PyQt5.QtWidgets `
  --hidden-import=PyQt5.QtPrintSupport `
  "--add-data=$workspace_root\src\i18n\drumburp_en.qm;i18n" `
  "--add-data=$workspace_root\src\i18n\drumburp_es.qm;i18n" `
  --distpath "$workspace_root\build\dist" `
  --specpath "$workspace_root\build\tmp" `
  --workpath "$workspace_root\build\tmp" `
  -i "$workspace_root\src\GUI\Icons\drumburp.ico" `
  "$workspace_root\src\DrumBurp.py"
Copy-Item "$workspace_root\COPYING.txt" "$workspace_root\build\dist"
Copy-Item "$workspace_root\build\DrumBurp.nsi" "$workspace_root\build\dist\"
Set-Location "$workspace_root\build\dist"
& "C:\Program Files (x86)\NSIS\makensis.exe" "$workspace_root\build\dist\DrumBurp.nsi"
Move-Item DrumBurp*setup.exe "$workspace_root\build\output" -Force
Set-Location "$workspace_root"

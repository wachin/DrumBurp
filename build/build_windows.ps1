# Build DrumBurp for Windows with Nuitka, then package it with NSIS.
#
# The script creates:
#   build/output/DrumBurp-<version>.0-setup.exe
#
# Linux and macOS still use their platform build scripts. This script only
# controls the official Windows package.

$ErrorActionPreference = "Stop"
Set-Item Env:PYTHONIOENCODING UTF-8

$workspace_root = Split-Path -Parent "$PSScriptRoot"
$dist_dir = Join-Path $workspace_root "build\dist"
$tmp_dir = Join-Path $workspace_root "build\tmp\nuitka"
$nuitka_output_dir = Join-Path $tmp_dir "output"
$output_dir = Join-Path $workspace_root "build\output"
$app_dist_dir = Join-Path $dist_dir "DrumBurp"
$version = (Get-Content "$workspace_root\VERSION" -Raw).Trim()
$windows_version = "$version.0"

Write-Output "Workspace root is $workspace_root"
Write-Output "Windows version is $windows_version"

New-Item -ItemType Directory -Force -Path $dist_dir, $tmp_dir, $nuitka_output_dir, $output_dir | Out-Null
Remove-Item "$dist_dir\*" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item "$nuitka_output_dir\*" -Recurse -Force -ErrorAction SilentlyContinue

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

    $searchRoots = @()
    if ($env:QTDIR) {
        $searchRoots += $env:QTDIR
    }
    $searchRoots += "C:\Qt"
    if ($env:USERPROFILE) {
        $searchRoots += (Join-Path $env:USERPROFILE "Qt")
    }

    foreach ($root in ($searchRoots | Select-Object -Unique)) {
        if (!(Test-Path $root)) {
            continue
        }
        $matches = Get-ChildItem -Path $root -Recurse -Filter lrelease.exe `
                                 -ErrorAction SilentlyContinue | `
            Sort-Object FullName -Descending
        if ($matches) {
            return $matches[0].FullName
        }
    }

    throw "Could not find lrelease. Install Qt translation tools, add lrelease to PATH, or install a Qt desktop kit under C:\Qt."
}

$lrelease = Get-LRelease

Write-Output "Compiling translations..."
& $lrelease "$workspace_root\src\i18n\drumburp_en.ts" -qm "$workspace_root\src\i18n\drumburp_en.qm"
& $lrelease "$workspace_root\src\i18n\drumburp_es.ts" -qm "$workspace_root\src\i18n\drumburp_es.qm"
& $lrelease "$workspace_root\src\i18n\drumburp_de.ts" -qm "$workspace_root\src\i18n\drumburp_de.qm"
& $lrelease "$workspace_root\src\i18n\drumburp_zh_TW.ts" -qm "$workspace_root\src\i18n\drumburp_zh_TW.qm"

& python -m nuitka `
  --standalone `
  --assume-yes-for-downloads `
  --remove-output `
  --msvc=latest `
  --enable-plugin=pyqt5 `
  --windows-console-mode=disable `
  --windows-icon-from-ico="$workspace_root\src\GUI\Icons\drumburp.ico" `
  --company-name="Whatang" `
  --product-name="DrumBurp" `
  --file-description="DrumBurp drum tab editor" `
  --file-version="$windows_version" `
  --product-version="$windows_version" `
  --copyright="Mike Thomas 2010-2019, Washington Indacochea Delgado 2026" `
  --include-data-dir="$workspace_root\src\i18n=i18n" `
  --output-filename="DrumBurp.exe" `
  --output-dir="$nuitka_output_dir" `
  "$workspace_root\src\DrumBurp.py"

$built_exe = Get-ChildItem -Path $nuitka_output_dir -Recurse -Filter "DrumBurp.exe" |
    Where-Object { $_.FullName -like "*.dist\DrumBurp.exe" } |
    Select-Object -First 1

if (-not $built_exe) {
    Write-Error "Nuitka output executable was not found."
}

Copy-Item $built_exe.Directory.FullName $app_dist_dir -Recurse -Force
Copy-Item "$workspace_root\COPYING.txt" "$dist_dir\" -Force

$nsi_content = Get-Content "$workspace_root\build\DrumBurp.nsi" -Raw
$nsi_content = $nsi_content.Replace('!define VERSION "1.1.3.0"', "!define VERSION `"$windows_version`"")
$nsi_content = $nsi_content.Replace('!define INSTALLER_NAME "DrumBurp-${VERSION}-setup.exe"', "!define INSTALLER_NAME `"DrumBurp-$windows_version-setup.exe`"")
Set-Content -Path "$dist_dir\DrumBurp.nsi" -Value $nsi_content -Encoding UTF8

$makensis = "C:\Program Files (x86)\NSIS\makensis.exe"
if (!(Test-Path $makensis)) {
    throw "NSIS was not found at $makensis"
}

Push-Location $dist_dir
& $makensis "$dist_dir\DrumBurp.nsi"
Move-Item "DrumBurp-*-setup.exe" "$output_dir" -Force
Pop-Location

Write-Output "Created installer in $output_dir"

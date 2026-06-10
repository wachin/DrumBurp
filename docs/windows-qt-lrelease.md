# Windows Qt Translation Tools (`lrelease`)

This note explains how DrumBurp finds `lrelease.exe` on Windows and how to
install the Qt components required to compile translation files (`.ts` ->
`.qm`).

## Why This Matters

DrumBurp stores editable translations in:

```text
src/i18n/*.ts
```

and compiled Qt translation binaries in:

```text
src/i18n/*.qm
```

The Windows build script:

```text
build/build_windows.ps1
```

compiles the `.ts` files before running PyInstaller.

If `lrelease.exe` is missing, the Windows build cannot regenerate the `.qm`
translation files.

## Use The Online Qt Installer

On Windows, install Qt using the official online installer:

- [Qt Online Installer (Open Source)](https://www.qt.io/development/download-qt-installer-oss)

Do not rely on a minimal offline Qt Creator-only install if you need to build
translations. Qt Creator by itself may not include the Qt translation tools.

## What To Install In Qt Maintenance Tool

Inside the Qt Maintenance Tool, make sure at least one full desktop Qt kit is
installed under:

```text
Qt for Development -> Qt -> <version> -> <desktop kit>
```

For example:

- `Qt 6.5.3 -> MinGW 11.2.0 64-bit`
- `Qt 6.5.3 -> MSVC 2019 64-bit`

Any normal desktop Qt kit is usually enough. The exact Qt version does not have
to match PyQt5 exactly just to run `lrelease.exe`.

## Typical Location Of `lrelease.exe`

After installing a desktop Qt kit, `lrelease.exe` is usually found in a path
like:

```text
C:\Qt\6.5.3\mingw_64\bin\lrelease.exe
```

or:

```text
C:\Qt\6.5.3\msvc2019_64\bin\lrelease.exe
```

To confirm it exists:

```powershell
Get-ChildItem C:\Qt -Recurse -Filter lrelease.exe
```

## How DrumBurp Finds `lrelease.exe`

`build/build_windows.ps1` now searches in this order:

1. `lrelease` already available in `PATH`
2. bundled Qt tools inside the active `PyQt5` installation
3. Qt tools from the optional Python package `qt5_applications`
4. standard Qt install roots on Windows:
   - `QTDIR`
   - `C:\Qt`
   - `%USERPROFILE%\Qt`

This makes the build more portable across different Windows developer machines
and different Qt versions.

## Manual Test

You can test `lrelease.exe` directly:

```powershell
& "C:\Qt\6.5.3\mingw_64\bin\lrelease.exe" .\src\i18n\drumburp_zh_TW.ts -qm .\src\i18n\drumburp_zh_TW.qm
```

Or simply run the project build script:

```powershell
pwsh -NoProfile -ExecutionPolicy Bypass -File .\build\build_windows.ps1
```

If the build script starts with:

```text
Compiling translations...
```

and updates the `.qm` files, then `lrelease.exe` was found successfully.

## Extra Notes For Windows Developers

- Installing Qt Creator is not the same as installing a full Qt desktop kit.
- If only Qt Creator is installed, `lrelease.exe` may be missing.
- If multiple Qt versions are installed, DrumBurp should use the first valid
  `lrelease.exe` it finds.
- If `lrelease.exe` exists but is not in `PATH`, that is fine; the build script
  still tries the common Qt locations automatically.
- If Windows blocks writing `.qm` files or PyInstaller temporary files, the
  problem is usually file locking, antivirus scanning, or a stale process, not
  a missing Qt installation.

## Related Files

- `build/build_windows.ps1`
- `src/i18n/i18n.py`
- `drumburp.pro`
- `ROADMAP_Win_Workflow.md`

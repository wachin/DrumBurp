# ROADMAP: Validate the Windows Workflow

This file is a practical guide for a developer to validate two things on a
Windows machine:

1. The PowerShell scripts in `build/` really work on Windows.
2. The real GitHub Actions workflow generates the Windows installer.

The real Windows validation should be done on Windows, because Linux cannot
fully verify:

- `pwsh`
- Chocolatey
- NSIS
- Windows paths using `\`
- the `.exe` installer
- the `DrumBurp.exe` smoke test

## Final Goal

At the end of this validation, the following should be confirmed:

- [x] DrumBurp can run from source on Windows 10.
- [x] Native Windows MIDI playback works through WinMM.
- [x] `MIDI -> Select MIDI out` is visible and can select Windows MIDI devices.
- [x] VirtualMIDISynth can be used as a Windows MIDI output device.
- [x] `pwsh` is installed and can run scripts.
- [ ] `build/install_windows.ps1` installs the required tools.
- [x] `build/build_windows.ps1` creates the installer.
- [x] The installer can be installed silently.
- [x] `DrumBurp.exe --pyinstaller-test` works.
- [ ] GitHub Actions generates the `db_windows` artifact.
- [ ] A `vX.Y.Z` tag can publish the installer in a GitHub Release.

## Completed: Windows MIDI Playback

DrumBurp now has native Windows MIDI playback through the Windows Multimedia
API (`winmm`). This avoids the `pygame`/PortMidi problem where devices such as
VirtualMIDISynth may appear in the device list but fail with `PortMidi: Host
error` or `midi Output not open`.

Confirmed behavior:

- [x] `BackendManager.output_drivers()` includes `winmm` and `Windows MM` on Windows.
- [x] `list_winmm_output_ports()` enumerates Windows MIDI output devices.
- [x] The MIDI menu shows devices such as `VirtualMIDISynth #1`,
  `Microsoft GS Wavetable Synth`, and `Microsoft MIDI Mapper`.
- [x] `VirtualMIDISynth #1` is preferred automatically when present.
- [x] Full score playback uses the selected WinMM output device.
- [x] Playback was tested with VirtualMIDISynth and the FluidR3 GM SoundFont.
- [x] Drum tablature playback sounds correct on tested `.brp` files.

Recommended Windows MIDI setup:

1. Install VirtualMIDISynth from `https://coolsoft.altervista.org/en/virtualmidisynth`.
2. Download one or more recommended SoundFonts from the same website.
3. Open VirtualMIDISynth settings.
4. On the **Soundfonts** tab, click **+** and add the SoundFont file.
5. Keep only one SoundFont active at a time for predictable playback.
6. Launch DrumBurp from the repository root:

```powershell
$env:PYTHONPATH = "$PWD\src"
py .\src\DrumBurp.py
```

7. In DrumBurp choose:

```text
MIDI -> Select MIDI out -> VirtualMIDISynth #1
```

## Windows Requirements

Install these before starting:

- [x] Git for Windows: `https://git-scm.com/download/win`
- [x] Python 3.11 x64: `https://www.python.org/downloads/`
- [x] PowerShell 7 (`pwsh`): `https://learn.microsoft.com/en-us/powershell/scripting/install/install-powershell-on-windows`
- [x] Chocolatey: `https://chocolatey.org/install`
- [x] NSIS: `https://nsis.sourceforge.io/Download`
- [x] GitHub CLI (`gh`), optional but recommended: `https://cli.github.com/`

What each requirement is used for:

- Git for Windows provides the `git` command used to clone the repository,
  inspect changes, create commits, switch branches, and push code to GitHub.
- Python 3.11 x64 is the Python runtime used to install DrumBurp's dependencies,
  run tests, and build the Windows executable with PyInstaller.
- PowerShell 7 provides the `pwsh` command used to run and validate the Windows
  build scripts in a modern, cross-platform PowerShell environment.
- Chocolatey provides the `choco` command used by the Windows install script to
  install external build tools such as NSIS and runtime dependencies.
- NSIS provides `makensis.exe`, which packages the PyInstaller output into the
  final Windows installer, for example `DrumBurp-X.Y.Z.0-setup.exe`.
- GitHub CLI provides the `gh` command used to inspect GitHub Actions runs,
  download build artifacts, inspect logs, and manage release-related GitHub
  operations from the terminal.

Git for Windows and GitHub CLI are different tools, and both are useful:

- Git for Windows talks to the Git repository. It handles source control tasks
  such as `git clone`, `git status`, `git commit`, `git pull`, and `git push`.
- GitHub CLI talks to GitHub as a hosting platform. It handles GitHub-specific
  tasks such as `gh run list`, `gh run watch`, `gh run download`, `gh release`,
  `gh issue`, and `gh pr`.

Install both because Git is required for normal repository work, while GitHub
CLI is the most convenient way to validate GitHub Actions artifacts and releases
without relying only on the browser.

After installing the Windows requirements, restart the computer before
continuing. This refreshes `PATH` so commands such as `choco`, `gh`, `pwsh`,
and other newly installed tools are available in new terminals.

After the restart, authenticate GitHub CLI before validating GitHub Actions:

```powershell
gh auth login
```

This is required before using commands such as `gh run list`, `gh run watch`,
or `gh run download`.

Useful commands:

```powershell
git --version
python --version
py -3 --version
pwsh --version
choco --version
makensis /VERSION
gh --version
```

If PowerShell 7 is missing:

```powershell
winget install Microsoft.PowerShell
```

On Windows 10 and newer, `powershell.exe` is Windows PowerShell and `pwsh.exe`
is PowerShell 7. The build validation uses `pwsh`, so install PowerShell 7
separately even if Windows PowerShell is already present.

This workflow is intended for Windows 10/11 development machines and supported
GitHub Actions Windows runners. Older unsupported Windows versions are not part
of this Windows build workflow.

If Chocolatey is missing, install it from:

```text
https://chocolatey.org/install
```

Then close and reopen PowerShell and verify:

```powershell
choco --version
```

If NSIS is missing, install it from:

```text
https://nsis.sourceforge.io/Download
```

The build script expects this executable:

```text
C:\Program Files (x86)\NSIS\makensis.exe
```

If GitHub CLI is missing:

```powershell
winget install GitHub.cli
```

## Recommended Validation Instruction

If a programming assistant performs this validation, open it on Windows inside
the repository folder and give it this instruction:

```text
Read ROADMAP_Win_Workflow.md and validate the DrumBurp Windows build.
First inspect git status, then validate PowerShell syntax with pwsh, install
dependencies if needed, run build/install_windows.ps1 and build/build_windows.ps1,
install the generated .exe into a temporary folder, and run
DrumBurp.exe --pyinstaller-test. Do not delete unrelated changes.
```

## Step 1: Inspect Repository State

- [x] Run `git status --short`.
- [x] Run `git branch --show-current`.
- [x] Note unrelated changes without reverting them.

```powershell
git status --short
git branch --show-current
```

If there are unrelated changes, do not revert them. Just note them.

## Step 2: Confirm That pwsh Exists

- [x] Run `pwsh --version`.
- [x] Confirm that it prints a PowerShell 7.x version.

```powershell
pwsh --version
```

## Step 3: Validate PowerShell Syntax

- [x] Parse `build/install_windows.ps1`.
- [x] Parse `build/build_windows.ps1`.
- [x] Parse `build/install_pyqt.ps1`.
- [x] Confirm there are no syntax errors.

This command parses the scripts without executing them:

```powershell
pwsh -NoProfile -Command @'
$files = @(
  "build/install_windows.ps1",
  "build/build_windows.ps1",
  "build/install_pyqt.ps1"
)

$failed = $false
foreach ($file in $files) {
  $tokens = $null
  $errors = $null
  [System.Management.Automation.Language.Parser]::ParseFile(
    (Resolve-Path $file),
    [ref]$tokens,
    [ref]$errors
  ) | Out-Null

  if ($errors.Count -gt 0) {
    Write-Host "Syntax errors in $file"
    $errors | Format-List
    $failed = $true
  } else {
    Write-Host "OK: $file"
  }
}

if ($failed) { exit 1 }
'@
```

Expected result:

```text
OK: build/install_windows.ps1
OK: build/build_windows.ps1
OK: build/install_pyqt.ps1
```

## Step 4: Create a Clean Python Environment

- [x] Create `.venv-win-build`.
- [x] Activate `.venv-win-build`.
- [x] Upgrade `pip`.
- [x] If Windows blocks `Activate.ps1`, use `ExecutionPolicy Bypass` only for the current process.

```powershell
py -3.11 -m venv .venv-win-build
.\.venv-win-build\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

If Windows blocks `Activate.ps1`, use:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv-win-build\Scripts\Activate.ps1
```

## Step 5: Install Build Dependencies

- [ ] Run `build/install_windows.ps1` successfully from an elevated/admin PowerShell.
- [x] Confirm that `PyQt5` and `pygame` import correctly.
- [x] Confirm that `pyinstaller` responds.
- [x] Confirm that `makensis` responds.
- [x] If `makensis` is not in `PATH`, locate `makensis.exe`.

Run PowerShell as administrator if Chocolatey requires it:

```powershell
pwsh -NoProfile -ExecutionPolicy Bypass -File .\build\install_windows.ps1
```

Verify tools:

```powershell
python -c "import PyQt5, pygame; print('Python deps OK')"
pyinstaller --version
makensis /VERSION
```

If `makensis` is not in `PATH`, check:

```powershell
Get-ChildItem "C:\Program Files*\NSIS\makensis.exe" -Recurse -ErrorAction SilentlyContinue
```

If `lrelease` is missing after installing PyQt5, install Qt tools in the active
environment:

```powershell
python -m pip install qt5-tools
$qtBin = python -c "import pathlib, qt5_applications; print(pathlib.Path(qt5_applications.__file__).parent / 'Qt' / 'bin')"
$env:PATH = "$qtBin;$env:PATH"
lrelease -version
```

## Step 6: Build Windows Locally

- [x] Run `build/build_windows.ps1`.
- [x] Confirm that `build\output\DrumBurp-X.Y.Z.0-setup.exe` is created.

```powershell
pwsh -NoProfile -ExecutionPolicy Bypass -File .\build\build_windows.ps1
```

Expected output:

```text
build\output\DrumBurp-X.Y.Z.0-setup.exe
```

Check:

```powershell
Get-ChildItem .\build\output\*.exe
```

## Step 7: Test the Local Installer

- [x] Install the `.exe` into a temporary folder.
- [x] Run `DrumBurp.exe --pyinstaller-test`.
- [x] Confirm that the exit code is `0`.

Use a temporary folder so a real installation is not touched:

```powershell
$version = Get-Content .\VERSION
$installer = ".\build\output\DrumBurp-$version.0-setup.exe"
$installDir = Join-Path $env:TEMP "DrumBurp-test-install"

Remove-Item $installDir -Recurse -Force -ErrorAction SilentlyContinue
Start-Process -FilePath $installer -ArgumentList "/S", "/D=$installDir" -Wait
& "$installDir\DrumBurp\DrumBurp.exe" --pyinstaller-test
```

Expected result: the command exits with code `0`.

Check the exit code:

```powershell
$LASTEXITCODE
```

## Step 8: Validate the Workflow YAML Locally

- [x] Install `PyYAML` if it is not installed.
- [x] Parse `.github/workflows/build.yml`.
- [x] Confirm that it prints `workflow yaml ok`.

If Python has PyYAML installed:

```powershell
python -m pip install PyYAML
$yamlCheck = @'
from pathlib import Path
import yaml
with Path(".github/workflows/build.yml").open(encoding="utf-8") as handle:
    yaml.safe_load(handle)
print("workflow yaml ok")
'@
$yamlCheck | python -
```

## Step 9: Test GitHub Actions on a Branch

- [x] Confirm GitHub Actions is enabled on github.com.
- [x] Confirm workflow permissions allow the release job to create releases.
- [ ] Push a normal branch, for example `dev`.
- [ ] Open the run in the **Actions** tab.
- [ ] Confirm that `build_windows` passes.
- [ ] Confirm that `test_windows` passes.
- [ ] Confirm that `build_linux` passes.
- [ ] Confirm that `test_linux` passes.
- [ ] Confirm that `build_macos` passes.
- [ ] Confirm that `test_macos` passes.

Push a normal branch before publishing a tag:

```powershell
git push origin dev
```

### Enable GitHub Actions on github.com

Before expecting the workflow to run, configure the repository on github.com:

1. Open the repository in the browser.
2. Go to **Settings**.
3. Go to **Actions**.
4. Open **General**.
5. Under **Actions permissions**, select **Allow all actions and reusable workflows**.
6. Under **Workflow permissions**, select **Read and write permissions**.
7. Enable **Allow GitHub Actions to create and approve pull requests** only if
   the project later needs workflows to create pull requests automatically.
8. Click **Save**.

The **Read and write permissions** setting is important because the release job
uses `GITHUB_TOKEN` to create a GitHub Release and upload artifacts.

Confirmed on github.com:

- [x] **Actions permissions** is set to **Allow all actions and reusable workflows**.
- [x] **Workflow permissions** is set to **Read and write permissions**.
- [x] **Allow GitHub Actions to create and approve pull requests** is enabled.

View the workflow on GitHub:

```text
https://github.com/wachin/DrumBurp/actions
```

With GitHub CLI:

```powershell
gh auth login
gh run list --workflow "Build DrumBurp" --limit 5
gh run watch
```

### GitHub Actions Windows Build Notes

GitHub Actions can create the Windows `.exe` installer for a release when the
workflow runs on a supported Windows hosted runner and installs the same tools
validated locally:

- Python 3.11 x64
- Chocolatey
- NSIS
- PyInstaller and the Windows Python requirements
- Qt translation tools that provide `lrelease`

Do not rely on a developer's local NSIS or Chocolatey installation for GitHub
Actions. The workflow must install everything it needs inside the runner.

The current workflow uses `windows-latest`, which is a supported GitHub-hosted
Windows runner. It should be able to produce the Windows installer if the
Windows job installs NSIS and has a working `lrelease` command. If the Actions
log fails at `lrelease`, add an explicit install step for `qt5-tools` or install
Qt tools through Chocolatey before compiling translations.

Older unsupported Windows versions are not suitable GitHub Actions targets for
this project. Use Windows 10/11 development machines or GitHub-hosted Windows
runners for release builds.

### Git for Windows HTTPS Crash

If `git push`, `git pull`, or `git ls-remote` opens a Windows error dialog for
`git-remote-https.exe`, update Git for Windows to the latest stable version from:

```text
https://git-scm.com/download/win
```

This is not caused by GitHub CLI or by the GitHub Actions workflow. It is the
Git HTTPS transport crashing locally. Updating Git for Windows is the preferred
fix. If the problem remains, try changing only this repository to the OpenSSL
backend:

```powershell
git config --local http.sslBackend openssl
```

Then test:

```powershell
git ls-remote https://github.com/wachin/DrumBurp HEAD
```

## Step 10: Download the Windows Artifact

- [ ] Download the `db_windows` artifact.
- [ ] Confirm that it contains `DrumBurp-X.Y.Z.0-setup.exe`.
- [ ] Test the downloaded installer the same way as in step 7.

With GitHub CLI, replace `RUN_ID` with the real id:

```powershell
gh run download RUN_ID -n db_windows -D .\artifacts\db_windows
Get-ChildItem .\artifacts\db_windows
```

This file should appear:

```text
DrumBurp-X.Y.Z.0-setup.exe
```

## Step 11: Test a Real Release

- [ ] Confirm that a normal branch build already passed.
- [ ] Create a `vX.Y.Z` tag.
- [ ] Push the tag to GitHub.
- [ ] Confirm that the tag workflow finishes successfully.
- [ ] Confirm that the GitHub Release is created.
- [ ] Confirm that the Release includes the Windows `.exe` installer.
- [ ] Confirm that the Release includes the Linux `DrumBurp` binary.
- [ ] Confirm that the Release includes the macOS zip.

Do this only after the normal branch build has passed.

```powershell
git tag vX.Y.Z
git push origin vX.Y.Z
```

Example:

```powershell
git tag v1.1.4
git push origin v1.1.4
```

Then check:

```text
https://github.com/wachin/DrumBurp/releases
```

The Release should include:

- [ ] Windows `.exe` installer
- [ ] Linux `DrumBurp` binary
- [ ] macOS `DrumBurp-X.Y.Z-macOS-x64.zip`

## Common Problems

### `pwsh` Does Not Exist

Install PowerShell 7:

```powershell
winget install Microsoft.PowerShell
```

Close and reopen the terminal.

### Chocolatey Cannot Install Packages

Open PowerShell as administrator and repeat:

```powershell
choco install vcredist2008
choco install nsis
```

### `lrelease` Is Not Found

`build/build_windows.ps1` tries to find `lrelease` in `PATH` and inside the
PyQt5 installation. If it fails, check:

```powershell
python -c "import pathlib, PyQt5; print(pathlib.Path(PyQt5.__file__).parent / 'Qt5' / 'bin')"
```

### NSIS Is Not Found

Check:

```powershell
Get-Command makensis -ErrorAction SilentlyContinue
Get-ChildItem "C:\Program Files*\NSIS\makensis.exe" -Recurse -ErrorAction SilentlyContinue
```

If it exists but is not in `PATH`, add it temporarily:

```powershell
$env:PATH = "C:\Program Files (x86)\NSIS;$env:PATH"
```

### Opening `build\DrumBurp.nsi` Directly Fails

`build\DrumBurp.nsi` is not meant to be compiled directly from the `build`
directory. It expects the PyInstaller output layout created by
`build\build_windows.ps1`.

The build script does this before running NSIS:

- Copies `COPYING.txt` into `build\dist`.
- Copies `build\DrumBurp.nsi` into `build\dist`.
- Ensures `build\dist\DrumBurp` exists from the PyInstaller build.
- Changes the working directory to `build\dist`.
- Runs `makensis.exe build\dist\DrumBurp.nsi`.

If the script is opened directly from NSIS as `build\DrumBurp.nsi`, NSIS may
fail with:

```text
LicenseData: open failed "COPYING.txt"
```

That does not mean the installer is broken. To compile manually, first run the
Windows build script, then open or compile:

```text
build\dist\DrumBurp.nsi
```

from the `build\dist` directory.

### GitHub Release Fails with 403

Check in GitHub:

1. **Settings**
2. **Actions**
3. **General**
4. **Workflow permissions**
5. **Read and write permissions**

Also confirm that `.github/workflows/build.yml` contains:

```yaml
permissions:
  contents: write
```

## Final Report

At the end, report a summary with:

- [x] Windows version
- [x] `pwsh` version
- [x] Python version
- [x] whether the PowerShell scripts parsed correctly
- [x] whether `build_windows.ps1` generated the installer
- [x] exact path to the local installer
- [x] result of `DrumBurp.exe --pyinstaller-test`
- [ ] link to the GitHub Actions run
- [ ] whether `db_windows` was downloaded and tested
- [x] any error with relevant logs

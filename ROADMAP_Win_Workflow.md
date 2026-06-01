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

- [ ] `pwsh` is installed and can run scripts.
- [ ] `build/install_windows.ps1` installs the required tools.
- [ ] `build/build_windows.ps1` creates the installer.
- [ ] The installer can be installed silently.
- [ ] `DrumBurp.exe --pyinstaller-test` works.
- [ ] GitHub Actions generates the `db_windows` artifact.
- [ ] A `vX.Y.Z` tag can publish the installer in a GitHub Release.

## Windows Requirements

Install these before starting:

- [ ] Git for Windows
- [ ] Python 3.11 x64
- [ ] PowerShell 7 (`pwsh`)
- [ ] Chocolatey
- [ ] GitHub CLI (`gh`), optional but recommended

Useful commands:

```powershell
git --version
python --version
py -3 --version
pwsh --version
choco --version
gh --version
```

If PowerShell 7 is missing:

```powershell
winget install Microsoft.PowerShell
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

- [ ] Run `git status --short`.
- [ ] Run `git branch --show-current`.
- [ ] Note unrelated changes without reverting them.

```powershell
git status --short
git branch --show-current
```

If there are unrelated changes, do not revert them. Just note them.

## Step 2: Confirm That pwsh Exists

- [ ] Run `pwsh --version`.
- [ ] Confirm that it prints a PowerShell 7.x version.

```powershell
pwsh --version
```

## Step 3: Validate PowerShell Syntax

- [ ] Parse `build/install_windows.ps1`.
- [ ] Parse `build/build_windows.ps1`.
- [ ] Parse `build/install_pyqt.ps1`.
- [ ] Confirm there are no syntax errors.

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

- [ ] Create `.venv-win-build`.
- [ ] Activate `.venv-win-build`.
- [ ] Upgrade `pip`.
- [ ] If Windows blocks `Activate.ps1`, use `ExecutionPolicy Bypass` only for the current process.

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

- [ ] Run `build/install_windows.ps1`.
- [ ] Confirm that `PyQt5` and `pygame` import correctly.
- [ ] Confirm that `pyinstaller` responds.
- [ ] Confirm that `makensis` responds.
- [ ] If `makensis` is not in `PATH`, locate `makensis.exe`.

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

## Step 6: Build Windows Locally

- [ ] Run `build/build_windows.ps1`.
- [ ] Confirm that `build\output\DrumBurp-X.Y.Z.0-setup.exe` is created.

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

- [ ] Install the `.exe` into a temporary folder.
- [ ] Run `DrumBurp.exe --pyinstaller-test`.
- [ ] Confirm that the exit code is `0`.

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

- [ ] Install `PyYAML` if it is not installed.
- [ ] Parse `.github/workflows/build.yml`.
- [ ] Confirm that it prints `workflow yaml ok`.

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

- [ ] Windows version
- [ ] `pwsh` version
- [ ] Python version
- [ ] whether the PowerShell scripts parsed correctly
- [ ] whether `build_windows.ps1` generated the installer
- [ ] exact path to the local installer
- [ ] result of `DrumBurp.exe --pyinstaller-test`
- [ ] link to the GitHub Actions run
- [ ] whether `db_windows` was downloaded and tested
- [ ] any error with relevant logs

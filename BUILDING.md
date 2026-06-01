# Building DrumBurp

This document explains how to build DrumBurp executables for Linux, Windows, and
macOS with GitHub Actions. It is written for developers who are comfortable with
source code, but who may be new to this repository's release workflow.

For the Spanish walkthrough, see `BUILDING_ES.md`.

## Short Summary

If the repository is hosted on GitHub, contains
`.github/workflows/build.yml`, and GitHub Actions is enabled, GitHub can build
DrumBurp automatically on GitHub-hosted virtual machines.

The current workflow builds:

- **Linux:** a standalone PyInstaller binary named `DrumBurp`.
- **Windows:** an `.exe` installer created with NSIS.
- **macOS:** a `.zip` containing `DrumBurp.app`.

You do not need all three operating systems installed locally to produce these
release files. GitHub uses hosted runners:

- `ubuntu-latest` for Linux
- `windows-latest` for Windows
- `macos-15-intel` for macOS Intel/x64

Useful official GitHub documentation:

- GitHub-hosted runners: <https://docs.github.com/actions/reference/runners/github-hosted-runners>
- `GITHUB_TOKEN` permissions: <https://docs.github.com/actions/security-for-github-actions/security-guides/automatic-token-authentication>

## Relevant Files

### `.github/workflows/build.yml`

This is the main GitHub Actions workflow. It tells GitHub:

1. Which operating systems to build on.
2. Which Python version to install.
3. Which dependencies to install.
4. Which tests to run.
5. Which scripts in `build/` to execute.
6. Which files to keep as temporary artifacts.
7. Which files to upload to a GitHub Release when a version tag is pushed.

### `build/`

The `build/` directory contains the scripts used by the workflow:

- `build/build_linux.sh` builds the Linux binary with PyInstaller.
- `build/build_windows.ps1` builds the Windows PyInstaller output and packages
  it into an NSIS installer.
- `build/build_macos.sh` builds `DrumBurp.app` with PyInstaller and packages it
  into a `.zip`.
- `build/install_linux.sh` installs local Linux build dependencies.
- `build/install_windows.ps1` installs local Windows build dependencies.
- `build/install_macos.sh` installs local macOS build dependencies.
- `build/requirements-linux.txt` lists Python packages for Linux builds.
- `build/requirements-windows.txt` lists Python packages for Windows builds.
- `build/requirements-macos.txt` lists Python packages for macOS builds.
- `build/DrumBurp.nsi` is the NSIS installer script for Windows.

### `.versionflow`

This configures `versionflow`, the helper used to keep the version number in
sync across:

- `VERSION`
- `src/DBVersionNum.py`
- `build/DrumBurp.nsi`

The `current_version` value should match the current project version.

## Push Behavior

The workflow runs on `push`, so it starts when commits or tags are pushed to
GitHub.

| What you push | What GitHub Actions does |
|---|---|
| A commit to a normal branch, for example `dev` | Builds and tests Linux, Windows, and macOS. Stores temporary artifacts. |
| A tag like `v1.1.3` or `v1.1.4` | Builds, tests, and creates a GitHub Release with attached files. |
| A direct commit to `master` | The workflow is configured to skip direct `master` branch pushes. |

## Artifacts vs Releases

GitHub Actions has two related but different output types.

### Artifacts

Artifacts are temporary files produced by one workflow run. They are useful for
testing a build before publishing an official version.

This repository stores artifacts for 7 days:

- `db_linux`
- `db_windows`
- `db_macos`

### Releases

A Release is an official GitHub publication. This workflow creates a Release
only when a tag beginning with `v` is pushed, for example:

```bash
git tag v1.1.3
git push origin v1.1.3
```

The Release uploads:

- `DrumBurp-1.1.3.0-setup.exe`
- `DrumBurp`
- `DrumBurp-1.1.3-macOS-x64.zip`

The version number changes according to `VERSION` and the pushed tag.

## First-Time GitHub Actions Setup

### 1. Enable Actions

In your GitHub repository:

1. Open the repository page.
2. Click **Actions**.
3. If GitHub asks whether you want to enable workflows, approve it.

### 2. Allow Release Creation

The workflow already contains:

```yaml
permissions:
  contents: write
```

That allows GitHub's automatic token to create Releases and upload assets. If
the Release job still fails with a 403 error, check the repository settings:

1. **Settings**
2. **Actions**
3. **General**
4. **Workflow permissions**
5. Select **Read and write permissions**
6. Save the change

### 3. Test on a Branch First

Before publishing an official Release, push a normal development branch:

```bash
git push origin dev
```

Then open:

```text
https://github.com/YOUR_USER/DrumBurp/actions
```

Open the newest run and confirm that all jobs finish successfully.

## Publishing a Release

### 1. Update the Version

The version must match in:

- `VERSION`
- `src/DBVersionNum.py`
- `build/DrumBurp.nsi`
- `.versionflow`

The preferred approach is to use `versionflow` from a development environment
where the development dependencies are installed:

```bash
pip install -r requirements-dev.txt
```

If you update the version manually, verify that all files contain the same
version number.

### 2. Commit the Version Change

Example:

```bash
git add VERSION src/DBVersionNum.py build/DrumBurp.nsi .versionflow
git commit -m "Bump version to 1.1.4"
```

### 3. Create the Tag

The tag must start with `v`:

```bash
git tag v1.1.4
```

### 4. Push the Branch and Tag

```bash
git push origin dev
git push origin v1.1.4
```

Pushing the tag triggers the full build, test, and release flow. If all test
jobs pass, GitHub creates the Release and uploads the executables.

## Workflow Jobs

### `build_linux`

Runs on `ubuntu-latest`.

1. Checks out the source code.
2. Installs Python 3.11.
3. Installs Qt tools needed to compile translations.
4. Installs Python dependencies from `build/requirements-linux.txt`.
5. Compiles `.qm` translation files.
6. Runs the unit tests.
7. Runs `build/build_linux.sh`.
8. Uploads `build/dist/DrumBurp` as the `db_linux` artifact.

### `test_linux`

Downloads `db_linux` and runs:

```bash
DrumBurp --pyinstaller-test
```

This checks that the PyInstaller binary starts far enough to import the main
application modules.

### `build_windows`

Runs on `windows-latest`.

1. Checks out the source code.
2. Installs Python 3.11 x64.
3. Installs the MSVC 2008 redistributable.
4. Installs NSIS.
5. Installs Python dependencies from `build/requirements-windows.txt`.
6. Adds PyQt5's Qt tools directory to `PATH`.
7. Compiles `.qm` translation files.
8. Runs `build/build_windows.ps1`.
9. Uploads the installer as the `db_windows` artifact.

### `test_windows`

Downloads the installer, installs it silently, and runs:

```cmd
DrumBurp.exe --pyinstaller-test
```

### `build_macos`

Runs on `macos-15-intel`.

1. Checks out the source code.
2. Installs Python 3.11 x64.
3. Installs Homebrew's `qt` package to provide `lrelease`.
4. Installs Python dependencies from `build/requirements-macos.txt`.
5. Compiles `.qm` translation files.
6. Runs the unit tests.
7. Runs `build/build_macos.sh`.
8. Uploads `DrumBurp-VERSION-macOS-x64.zip` as the `db_macos` artifact.

### `test_macos`

Downloads the `.zip`, extracts it, and runs:

```bash
DrumBurp.app/Contents/MacOS/DrumBurp --pyinstaller-test
```

### `release`

Runs only when the pushed ref is a tag beginning with `v`.

It downloads all three artifacts and creates a GitHub Release with:

- the Windows installer
- the Linux binary
- the macOS `.zip`

## Important Limitations

### macOS Is Not Signed or Notarized

The `DrumBurp.app` generated by GitHub Actions is not signed with an Apple
Developer certificate and is not notarized by Apple.

That means macOS may show a security warning the first time a user opens it. A
more polished macOS distribution would require:

1. An Apple Developer account.
2. Signing certificates.
3. GitHub Actions secrets for those certificates.
4. Code signing.
5. Apple notarization.

This is not required to prove that the build works, but it matters for a
smoother end-user macOS release.

### The Current macOS Build Is x64

The workflow uses `macos-15-intel`, so it creates an Intel/x64 macOS app. On
Apple Silicon Macs it may run through Rosetta, but it is not a native ARM build.

A future workflow can add an Apple Silicon job and publish a second archive,
for example `macOS-arm64`.

### Linux Does Not Create a `.deb`

The Linux build creates a standalone PyInstaller binary. It does not currently
create a `.deb`, `.rpm`, AppImage, or Flatpak.

### Windows Creates an Installer

Windows uses PyInstaller to create the application directory and NSIS to create
an `.exe` installer. The installer creates shortcuts and an uninstaller.

## Local Builds

GitHub Actions is recommended for releases, but local builds are still useful
for debugging.

### Linux

```bash
bash build/install_linux.sh
bash build/build_linux.sh
```

Expected output:

```text
build/dist/DrumBurp
```

### Windows

In PowerShell:

```powershell
.\build\install_windows.ps1
.\build\build_windows.ps1
```

Expected output:

```text
build\output\DrumBurp-X.Y.Z.0-setup.exe
```

### macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
bash build/install_macos.sh
bash build/build_macos.sh
```

Expected output:

```text
build/output/DrumBurp-X.Y.Z-macOS-x64.zip
```

## Troubleshooting

### The Actions Tab Does Not Appear

Check that the repository is on GitHub and that this file exists:

```text
.github/workflows/build.yml
```

### The Workflow Does Not Create a Release

Confirm that you pushed a tag beginning with `v`:

```bash
git tag -l
git push origin v1.1.4
```

### Release Fails with a 403 Error

Check **Settings -> Actions -> General -> Workflow permissions** and use
**Read and write permissions**.

### `lrelease` Fails

`lrelease` compiles Qt translation files from `.ts` to `.qm`.

- On Linux it comes from `qttools5-dev-tools`.
- On macOS it comes from `brew install qt`.
- On Windows it is usually found in PyQt5's Qt tools directory after installing
  PyQt5 with `pip`.

### PyInstaller Fails

Read the failed job log first. PyInstaller failures are usually caused by a
missing dependency, missing data file, or hidden import. The scripts in `build/`
are the first place to adjust those settings.

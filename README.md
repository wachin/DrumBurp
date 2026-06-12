# DrumBurp

- Copyright (C) 2011-2019 Michael Thomas  
- Python 3 / PyQt5 fork and modifications (C) 2024-2026 Washington Indacochea Delgado  

DrumBurp is a simple GUI for creating and editing music notation for drum kit.

DrumBurp's aim is to make the user-experience of writing drum music as quick
and intuitive as possible. The generality of many existing music notation
software packages means that there is an abundance of unnecessary complexity
involved in writing drum notation. While these packages can produce beautiful
output, and cope with everything you could ever possibly want to notate, they
can be slow and ponderous to use. By being very clear that the objective of
DrumBurp is restricted to writing *only* drum music, I hope to remove the
difficulties such generality can impose.

DrumBurp will never have a Bagpipes mode.

The fundamental philosophy of DrumBurp is as follows: when faced with a choice
between additional functionality/complexity in a specific case, or speed,
simplicity and intuitive user interaction in the general case, the general case
always wins. Simple, quick and stupid is better than complex, slow and clever.

DrumBurp is focused around using a simple representation of drum music. For
each note you play it essentially cares about:

- **Which** drum you hit
- **When** you hit it
- **How** you strike it

These three pieces of information together are sufficient to write drum music
in tablature notation. DrumBurp aims to allow the drummer to get this
information into the computer as quickly and as painlessly as possible.

DrumBurp stores this information in its own format in its saved score files.
However, it can export tablature as ASCII text files easily enough. A long-term
goal of DrumBurp is to be able to output "real" drum notation as aesthetically
pleasing and easy to read as that produced by Lilypond or Nted.

DrumBurp's fundamental data structures should rarely, if ever, change. The most
important part of DrumBurp is its interface with the user. Its goal for the
user is less time writing, more time drumming.

---

## This fork — port to Python 3 / PyQt5 (version 1.1.3)

Fork of [DrumBurp](https://github.com/Whatang/DrumBurp) by Washington Indacochea Delgado.  
Complete port from PyQt4/Python 2 to PyQt5/Python 3

### Platform status

|           Platform            |          Status           |
| ----------------------------- | ------------------------- |
| Linux                         | Tested                    |
| Windows 10/11                 | Tested                    |
| macOS Big Sur 11.7.x          | Tested                    |
| GitHub Actions macOS 15 Intel | Build + Smoke Test Passed |

### Tested Linux distributions

- Debian 12
- MX Linux 23
- Ubuntu 26.04
- Ubuntu Studio 26.04

---

📖 **[Full manual → GitHub Wiki](https://github.com/wachin/DrumBurp/wiki)**

---

## Running from source, in plain words

DrumBurp can be used with all its features directly from this source code
folder. You do not need to compile it or build an installer first.

This is normal for many Python programs: Python reads the program files and runs
them directly. In practice, once Python and the required packages are installed,
the DrumBurp folder works much like a portable program folder. You can launch it
from the folder with `./run-drumburp.sh` on Linux, with
`run-drumburp.bat` on Windows, with `run-drumburp.command` on macOS, or with the
Python commands shown below.

What still has to be installed depends on the operating system:

- **Linux:** Python 3 is usually already installed, but DrumBurp still needs the
  PyQt5 and pygame packages listed below.
- **Windows:** install Python first, then install the Python packages with
  `pip`.
- **macOS:** do not rely on Apple's system Python; install a current Python
  version first, for example with Homebrew, then install the Python packages
  with `pip`.

Recommended Python versions:

- Use Python 3.11 x64 for release builds and PyInstaller packaging.
- Python 3.13 is also tested for running from source and for the unit test
  suite.

# Run on Linux

## Debian/Ubuntu tested in

This program has been tested on:

- Debian 12 
- MX Linux 23
- Ubuntu 26.04

Install dependencies:

```bash
sudo apt install python3-pyqt5 python3-pygame pyqt5-dev-tools lilypond
```

- `python3-pygame` — required for MIDI playback
- `pyqt5-dev-tools` — includes `pyuic5` and `pyrcc5` (only needed if regenerating UI/QRC files)
- `lilypond` — optional, for score export and preview

### Launch

In the root folder:

```bash
./run-drumburp.sh
```

or by double-clicking, but make sure the file is marked as executable (by right-clicking and in the "Permissions" tab marking it as executable)

Or run:

```bash
export PYTHONPATH="$PWD/src"
python3 src/DrumBurp.py
```

---

## Run in Ubuntu Studio

Tested on:

* [Ubuntu Studio 26.04](https://ubuntustudio.org/)

### MIDI playback with JACK and Qsynth

DrumBurp from source has been tested successfully with:

* JACK (via QjackCtl)
* Qsynth
* General MIDI SoundFont

Important: the startup order matters.

The following sequence works correctly:

1. Start **QjackCtl**.
2. Verify that the JACK server is running.
3. Start **Qsynth**.
4. Load a General MIDI SoundFont.
5. Click **Start** in Qsynth if needed.
6. Launch DrumBurp.
7. Open a score.
8. Press **Play**.

MIDI playback should now work correctly.

### Known issue

The following startup order was tested and did **not** work reliably:

1. Start Qsynth.
2. Start QjackCtl.
3. Launch DrumBurp.

When Qsynth is started before JACK is available, DrumBurp may fail to play MIDI correctly.

For best results, always start JACK first and then start Qsynth.

---

## Run in AV Linux

---

## Linux MIDI with JACK with a SoundFont synth

On Linux, DrumBurp sends MIDI through the available MIDI backend. If you not use UbuntuStudio or not use AV Linux, and you can want a better sound quality, is possible to use an external synth such as Qsynth (not tested FluidSynth, TiMidity, or another JACK/ALSA MIDI target). To do this your Linux Operative System need a Kernel Real Time and enabled JACK, you can follow this tutorial to setup all need (the tutorial are in spanish, use an translator):

**Cómo instalar y usar Jack Audio Connection Kit JACK + Ardour y sus plugins con un Kernel Tiempo Real en MX Linux, Debian**  
[https://facilitarelsoftwarelibre.blogspot.com/2020/10/instalar-realtime-kernel-en-mx-linux.html](https://facilitarelsoftwarelibre.blogspot.com/2020/10/instalar-realtime-kernel-en-mx-linux.html)    

Typical JACK/SoundFont workflow:

1. Start JACK.
2. Start Qsynth or FluidSynth and load a General MIDI SoundFont.
3. Open DrumBurp.
4. Use `MIDI -> Refresh Device List` if the synth was started after DrumBurp.
5. Choose the synth from `MIDI -> Select MIDI out`.
6. Play the score.

DrumBurp does not manage SoundFont files itself; the external synth owns that
part of the setup.

---

# Run on Windows 10

First of all you need to install Python [Python](https://www.python.org/downloads/) and during setup select install to `PATH`

Open **PowerShell** in the repository root and install the Python packages with
`py -m pip`:

```powershell
py -m pip install --upgrade pip
py -m pip install -r build\requirements-windows.txt
```

The Windows package names are:

- `PyQt5` — Qt GUI bindings; includes Qt modules such as `QtWidgets`,
  `QtPrintSupport` and `QtMultimedia`
- `PyQt5-sip` — support package used by PyQt5
- `pygame` — MIDI fallback support; Windows playback uses the native WinMM
  backend
- `pywin32` — Windows support package used by the build environment
- `pyinstaller` — only needed to build a standalone `.exe`
- `pylint` — only needed for development checks

If you only want to test the program from source, this smaller install is
usually enough:

```powershell
py -m pip install PyQt5 PyQt5-sip pygame
```

After installing the dependencies, you can launch DrumBurp by double-clicking
`run-drumburp.bat` in the repository folder.

The Windows launcher sets `PYTHONPATH` automatically and starts
`src\DrumBurp.py` from the repository root. It preserves normal DrumBurp
settings, including `File -> Recent Scores...`, so it can be used as the usual
development launcher.

Or run DrumBurp from PowerShell:

```powershell
$env:PYTHONPATH = "$PWD\src"
py .\src\DrumBurp.py
```

DrumBurp score files use the `.brp` extension. The program filters recent
scores and drag-and-drop input so unsupported files such as `.md`, `.txt`,
`.pdf`, or images are not opened as scores.

## MIDI playback on Windows with VirtualMIDISynth

For good MIDI sound on Windows, install
[CoolSoft VirtualMIDISynth](https://coolsoft.altervista.org/en/virtualmidisynth).
VirtualMIDISynth provides a Windows MIDI output device and handles SoundFont
loading outside DrumBurp.

After installing VirtualMIDISynth:

1. Download one or more of the recommended SoundFonts from the VirtualMIDISynth
   website.
2. Open the VirtualMIDISynth configuration window.
3. On the **Soundfonts** tab, click the **+** button.
4. Select the SoundFont file you downloaded and add it.
5. Enable only the SoundFont you want to use. VirtualMIDISynth can list several
   SoundFonts, but only one should be active at a time for predictable playback.

Launch DrumBurp from the repository root:

```powershell
$env:PYTHONPATH = "$PWD\src"
py .\src\DrumBurp.py
```

Then choose:

```text
MIDI -> Select MIDI out -> VirtualMIDISynth #1
```

DrumBurp uses the native Windows Multimedia API (`winmm`) on Windows, so
VirtualMIDISynth should play drum tablature correctly without FluidSynth or any
SoundFont loaded inside DrumBurp itself.

To run the test suite on Windows:

```powershell
$env:PYTHONPATH = "$PWD\src"
py -m unittest discover -s src\test
```

The same launcher can be used for a quick smoke test:

```powershell
.\run-drumburp.bat --pyinstaller-test
```

### Windows build environment

For release builds on Windows, use Python 3.11 x64 and install the build
requirements:

```powershell
py -3.11 -m pip install --upgrade pip
py -3.11 -m pip install -r build\requirements-windows.txt
```

The Windows installer build also requires PowerShell 7, Chocolatey, NSIS, Git
for Windows, and GitHub CLI. See `ROADMAP_Win_Workflow.md` for the detailed
Windows validation workflow. For the Qt translation tool (`lrelease.exe`) on
Windows, see `docs/windows-qt-lrelease.md`.

### Manual GitHub Actions validation

If GitHub CLI is authenticated, the build workflow can be launched manually:

```powershell
gh workflow run "Build DrumBurp" --ref master
gh run list --workflow "Build DrumBurp" --limit 5
gh run watch
```

Manual runs validate the Windows, Linux, and macOS builds and smoke tests. The
release job only publishes assets when the workflow is triggered by a version
tag such as `v1.1.4`.

Optional features:

- **LilyPond/PDF export:** install LilyPond for Windows from
  `https://lilypond.org/`, then set the path to `lilypond.exe` inside
  DrumBurp's Lilypond options.
- **MIDI playback:** VirtualMIDISynth is recommended. Windows may also provide
  Microsoft GS Wavetable Synth or Microsoft MIDI Mapper, but VirtualMIDISynth
  with a General MIDI SoundFont usually sounds better.

# Run on macOS

These instructions are intended for running DrumBurp from source on macOS.

## Tested macOS versions

DrumBurp has been successfully tested on:

* macOS Big Sur 11.7.x (Intel)
* Python 3.12.9
* PyQt5 5.15.11
* pygame 2.5.2

In addition, the GitHub Actions continuous integration workflow successfully builds and smoke-tests DrumBurp on:

* macOS 15 (Intel runner)
* Python 3.11

## Install Python

Do not rely on Apple's bundled Python.

Download and install Python from:

[https://www.python.org/downloads/macos/](https://www.python.org/downloads/macos/)

Recommended versions:

* Python 3.11.x (recommended for release builds and PyInstaller)
* Python 3.12.x (tested successfully)

Python 3.13 is tested by the automated unit tests in GitHub Actions.

Python 3.14 has not yet been tested and is currently not recommended.

Verify the installation:

```bash
python3 --version
```

## Optional: install Git

If Git is not installed, first install Homebrew:

[https://brew.sh/](https://brew.sh/)

Then install Git:

```bash
brew install git
```

Verify:

```bash
git --version
```

## Install DrumBurp dependencies

From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate

python3 -m pip install --upgrade pip
python3 -m pip install PyQt5 PyQt5-sip pygame
```

### Important: Always use `python3` command on macOS.

Do not use the command `python`, because some macOS installations still provide
an older system Python that may not be compatible with DrumBurp.

## Run DrumBurp

```bash
export PYTHONPATH="$PWD/src"
python3 src/DrumBurp.py
```

After installing the dependencies, you can also launch DrumBurp by double-clicking:

```text
run-drumburp.command
```

If macOS says the launcher is not executable, run:

```bash
chmod +x run-drumburp.command
```

## Leaving the virtual environment

When you are finished using DrumBurp, you can leave the virtual environment by running:

```bash
deactivate
```

Your Terminal prompt should return to normal and the `(.venv)` prefix will disappear.

## Running DrumBurp again later

You only need to create the virtual environment once.

The next time you want to run DrumBurp, open a Terminal in the repository folder and activate the existing environment:

```bash
cd ~/Dev/DrumBurp
source .venv/bin/activate
```

Then launch DrumBurp:

```bash
export PYTHONPATH="$PWD/src"
python3 src/DrumBurp.py
```

You do **not** need to run:

```bash
python3 -m venv .venv
```

again unless:

* you deleted the `.venv` folder,
* you installed a different Python version,
* or the environment became corrupted.

## Updating dependencies later

If the project requirements change in a future version, activate the virtual environment and run:

```bash
python3 -m pip install --upgrade pip
python3 -m pip install PyQt5 PyQt5-sip pygame
```

or install the updated requirements file if one is provided.

## Checking that the virtual environment is active

When the environment is active, your prompt will usually look similar to:

```text
(.venv) username@computer DrumBurp %
```

The `(.venv)` prefix indicates that Python packages will be installed inside the DrumBurp environment rather than system-wide.


## Notes

* MIDI playback has been tested successfully on macOS Big Sur 11.7.x.
* DrumBurp uses pygame for MIDI playback on macOS.
* If playback is silent, verify that macOS has an available audio/MIDI output device.
* Exporting a `.mid` file is a useful way to verify MIDI generation.


Optional features:

- **LilyPond/PDF export:** install LilyPond for macOS from
  `https://lilypond.org/`, then set the path to the `lilypond` executable
  inside DrumBurp's Lilypond options.
- **MIDI playback:** DrumBurp uses `pygame`. If   DrumBurp starts but playback is silent, check that macOS has an available  MIDI/audio output device and try exporting a `.mid` file to verify that MIDI generation is working.

# MIDI playback

DrumBurp produces MIDI sound through the native Windows Multimedia API (`winmm`)
on Windows and through `pygame` on other platforms. On Windows, this allows
playback through MIDI output devices such as VirtualMIDISynth, Microsoft GS
Wavetable Synth, or other Windows MIDI ports. DrumBurp does not load SoundFonts
itself; external synths such as VirtualMIDISynth handle that.

---

# What changed from the original

- Complete port from PyQt4 to PyQt5: all imports, signals, slots and resources
- Port from Python 2 to Python 3: integer division, `base64`, comparisons, `exec()`, etc.
- UI files regenerated with `pyuic5`; QRC resources regenerated with `pyrcc5`
- Temporary compatibility layer `src/PyQt4/` removed
- PDF export via LilyPond 2.24 fixed
- Native Windows MIDI playback via WinMM added, including selectable MIDI output
  devices such as VirtualMIDISynth
- Integer division in MIDI and Lilypond calculations fixed
- About dialog updated with port credits
- Version updated to 1.1.3

See `migration_report_pyqt5.md` for the full technical details.

📖 **[Tutorial → GitHub Wiki](https://github.com/wachin/DrumBurp/wiki)**  
🐛 **[Bugs report](https://github.com/wachin/DrumBurp/issues)**

# License

DrumBurp is free software: you can redistribute it and/or modify it under the
terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program. If not, see <https://www.gnu.org/licenses/>.

See the file `COPYING.txt` for the full text of the GNU GPL.

**Original author:** Michael Thomas — drumburp@whatang.org  
**PyQt5 port:** Washington Indacochea Delgado — linuxfrontier@proton.me

---

# Internationalization (i18n) — for developers

DrumBurp supports multiple languages via Qt Linguist and `.qm` translation files.

## Install required tools

```bash
sudo apt install pyqt5-dev-tools qttools5-dev-tools
# provides: pylupdate5, lrelease, linguist
```

## Translation files

```
drumburp.pro              Qt project file — lists all source files for pylupdate5
src/i18n/
  i18n.py                 Translation loader (called at startup)
  drumburp_en.ts          English reference (source of truth)
  drumburp_es.ts          Spanish translation
  drumburp_de.ts          German translation
  drumburp_zh_TW.ts       Traditional Chinese translation
  drumburp_en.qm          Compiled English binary
  drumburp_es.qm          Compiled Spanish binary
  drumburp_de.qm          Compiled German binary
  drumburp_zh_TW.qm       Compiled Traditional Chinese binary
```

### Update strings after editing source code

```bash
# Re-extract all strings from Python and .ui files
pylupdate5 drumburp.pro

# Recompile after translating
lrelease src/i18n/drumburp_en.ts -qm src/i18n/drumburp_en.qm
lrelease src/i18n/drumburp_es.ts -qm src/i18n/drumburp_es.qm
lrelease src/i18n/drumburp_de.ts -qm src/i18n/drumburp_de.qm
lrelease src/i18n/drumburp_zh_TW.ts -qm src/i18n/drumburp_zh_TW.qm
```

On Windows, see `docs/windows-qt-lrelease.md` for the Qt Creator/Qt installer
requirements and how `build/build_windows.ps1` locates `lrelease.exe`.

### Translate using Qt Linguist GUI

```bash
linguist src/i18n/drumburp_es.ts
linguist src/i18n/drumburp_de.ts
linguist src/i18n/drumburp_zh_TW.ts
```

### Test in a specific language

```bash
# Spanish
LANGUAGE=es ./run-drumburp.sh
./run-drumburp.sh --language es

# German
LANGUAGE=de ./run-drumburp.sh
./run-drumburp.sh --language de

# Traditional Chinese
LANGUAGE=zh_TW ./run-drumburp.sh
./run-drumburp.sh --language zh_TW

# Force English explicitly
./run-drumburp.sh --language en

# Use system locale
./run-drumburp.sh
```

### Add a new language (e.g. French)

1. Add `src/i18n/drumburp_fr.ts` to `drumburp.pro` under `TRANSLATIONS`
2. Run `pylupdate5 drumburp.pro` — creates the new `.ts` file
3. Translate with `linguist src/i18n/drumburp_fr.ts`
4. Run `lrelease src/i18n/drumburp_fr.ts -qm src/i18n/drumburp_fr.qm`
5. Test with `LANGUAGE=fr ./run-drumburp.sh`

See `ROADMAP_i18n.md` for the full i18n plan and progress.

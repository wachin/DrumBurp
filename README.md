# DrumBurp

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

# Run on Windows 10

These instructions assume Python is already installed and available on `PATH`.
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
- `pygame` — MIDI playback support
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

Or run DrumBurp from PowerShell:

```powershell
$env:PYTHONPATH = "$PWD\src"
py .\src\DrumBurp.py
```

To run the test suite on Windows:

```powershell
$env:PYTHONPATH = "$PWD\src"
py -m unittest discover -s src\test
```

Optional features:

- **LilyPond/PDF export:** install LilyPond for Windows from
  `https://lilypond.org/`, then set the path to `lilypond.exe` inside
  DrumBurp's Lilypond options.
- **MIDI playback:** Windows normally provides a MIDI output device such as
  Microsoft GS Wavetable Synth. If DrumBurp starts but MIDI is silent, check
  that Windows has an active MIDI output device; MIDI export can still be tested
  without extra system packages.

# Run on macOS

These instructions are intended for testing DrumBurp from source on macOS.
Install Python first, for example with Homebrew:

```bash
brew install python
```

From the repository root, create a virtual environment and install the Python
packages:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install PyQt5 PyQt5-sip pygame
```

Run DrumBurp:

```bash
export PYTHONPATH="$PWD/src"
python src/DrumBurp.py
```

After installing the dependencies, you can also launch DrumBurp by
double-clicking `run-drumburp.command` in the repository folder. If macOS says
the launcher is not executable, run this once from Terminal:

```bash
chmod +x run-drumburp.command
```

Optional features:

- **LilyPond/PDF export:** install LilyPond for macOS from
  `https://lilypond.org/`, then set the path to the `lilypond` executable
  inside DrumBurp's Lilypond options.
- **MIDI playback:** DrumBurp uses `pygame`, not JACK or TiMidity directly. If
  DrumBurp starts but playback is silent, check that macOS has an available
  MIDI/audio output device and try exporting a `.mid` file to verify that MIDI
  generation is working.

## MIDI playback

DrumBurp produces MIDI sound with `pygame`. Short preview notes are sent through
`pygame.midi` to the default MIDI output device. Full score playback is generated
as a MIDI file in memory and played through `pygame.mixer.music`.

---

## What changed from the original

- Complete port from PyQt4 to PyQt5: all imports, signals, slots and resources
- Port from Python 2 to Python 3: integer division, `base64`, comparisons, `exec()`, etc.
- UI files regenerated with `pyuic5`; QRC resources regenerated with `pyrcc5`
- Temporary compatibility layer `src/PyQt4/` removed
- PDF export via LilyPond 2.24 fixed
- Integer division in MIDI and Lilypond calculations fixed
- About dialog updated with port credits
- Version updated to 1.1.3

See `migration_report_pyqt5.md` for the full technical details.

📖 **[Manual completo → GitHub Wiki](https://github.com/wachin/DrumBurp/wiki)**  
🐛 **[Reportar problemas](https://github.com/wachin/DrumBurp/issues)**

## License

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

## Internationalization (i18n) — for developers

DrumBurp supports multiple languages via Qt Linguist and `.qm` translation files.

### Install required tools

```bash
sudo apt install pyqt5-dev-tools qttools5-dev-tools
# provides: pylupdate5, lrelease, linguist
```

### Translation files

```
drumburp.pro              Qt project file — lists all source files for pylupdate5
src/i18n/
  i18n.py                 Translation loader (called at startup)
  drumburp_en.ts          English reference (source of truth)
  drumburp_es.ts          Spanish translation
  drumburp_en.qm          Compiled English binary
  drumburp_es.qm          Compiled Spanish binary
```

### Update strings after editing source code

```bash
# Re-extract all strings from Python and .ui files
pylupdate5 drumburp.pro

# Recompile after translating
lrelease src/i18n/drumburp_en.ts -qm src/i18n/drumburp_en.qm
lrelease src/i18n/drumburp_es.ts -qm src/i18n/drumburp_es.qm
```

### Translate using Qt Linguist GUI

```bash
linguist src/i18n/drumburp_es.ts
```

### Test in a specific language

```bash
# Spanish
LANGUAGE=es ./run-drumburp.sh
./run-drumburp.sh --language es

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

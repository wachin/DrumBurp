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
Complete port from PyQt4/Python 2 to PyQt5/Python 3, tested on Debian 12 / MX Linux 23 / UbuntuStudio.

📖 **[Full manual → GitHub Wiki](https://github.com/wachin/DrumBurp/wiki)**

## Install dependencies

```bash
sudo apt install python3-pyqt5 python3-pygame python3-pyqt5.qtmultimedia \
                 pyqt5-dev-tools lilypond fluid-soundfont-gm
```

- `python3-pyqt5.qtmultimedia` — required for MIDI playback
- `pyqt5-dev-tools` — includes `pyuic5` and `pyrcc5` (only needed if regenerating UI/QRC files)
- `lilypond` — optional, for score export and preview
- `fluid-soundfont-gm` — General MIDI soundfont (required for MIDI)

## Run

```bash
./run-drumburp.sh
```

Or manually:

```bash
export PYTHONPATH="$PWD/src"
python3 src/DrumBurp.py
```

## MIDI playback on Linux

For DrumBurp to produce MIDI sound you need an active virtual synthesiser.
The recommended approach depends on your operating system.

### Recommended option — Qsynth with JACK (UbuntuStudio / AV Linux)

The most convenient way is to use an audio-oriented operating system such as:

- **[Ubuntu Studio](https://ubuntustudio.org/)** — includes JACK and Qsynth pre-configured
- **[AV Linux](https://www.bandshed.net/)** — another excellent option for professional audio on Linux

On these systems all you need to do is:

1. Start JACK (or let it start automatically at login)
2. Open **Qsynth** and load the soundfont `FluidR3_GM.sf2`
   (included in the `fluid-soundfont-gm` package, typical path:
   `/usr/share/sounds/sf2/FluidR3_GM.sf2`)
3. Launch DrumBurp — it will detect the synthesiser automatically

### Alternative option — TiMidity (any Debian/Ubuntu distro)

If JACK is not available you can use TiMidity as a virtual synthesiser:

**1. Install:**

```bash
sudo apt install timidity fluid-soundfont-gm alsa-utils
```

**2. Load the MIDI sequencer kernel module:**

```bash
modprobe snd_seq
```

**3. Start TiMidity in server mode:**

```bash
timidity -iA -Os -B2,8 &
```

This starts TiMidity in the background listening on ALSA ports (typically `128:0`).
You can verify it with `aconnect -l`.

**4. Launch DrumBurp** — it will detect the active MIDI ports automatically.

**To stop TiMidity when you are done:**

```bash
killall timidity
```

> **Note:** The `modprobe snd_seq` command activates the kernel MIDI sequencer.
> Without it, programs cannot connect to each other to send MIDI notes.
> On UbuntuStudio and AV Linux this is already active by default.

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

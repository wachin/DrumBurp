# DrumBurp 1.1.3 — port to Python 3 / PyQt5

Fork of [DrumBurp](https://github.com/Whatang/DrumBurp) by Washington Indacochea Delgado.  
Complete port from PyQt4/Python 2 to PyQt5/Python 3, tested on Debian 12 / MX Linux 23 / UbuntuStudio.

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

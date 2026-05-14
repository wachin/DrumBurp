# MIDI Playback

DrumBurp can play back your score through MIDI using your system's
synthesiser.

---

## Requirements

Install the MIDI support package:

```bash
sudo apt install python3-pyqt5.qtmultimedia fluid-soundfont-gm
```

---

## Recommended setup — Qsynth with JACK

The most reliable setup is to use an audio-oriented Linux distribution:

- **[Ubuntu Studio](https://ubuntustudio.org/)** — includes JACK and Qsynth
  pre-configured
- **[AV Linux](https://www.bandshed.net/)** — another excellent option

Steps:
1. Start JACK (or let it start automatically at login)
2. Open **Qsynth** and load the soundfont `FluidR3_GM.sf2`
   (path: `/usr/share/sounds/sf2/FluidR3_GM.sf2`)
3. Launch DrumBurp — it will detect the synthesiser automatically

---

## Alternative setup — TiMidity

If JACK is not available:

```bash
# Install
sudo apt install timidity fluid-soundfont-gm alsa-utils

# Load the MIDI sequencer kernel module
modprobe snd_seq

# Start TiMidity in server mode (background)
timidity -iA -Os -B2,8 &

# Stop when done
killall timidity
```

---

## Playing back a score

- **MIDI → Play Score** — plays the whole score from start to finish
- **MIDI → Loop Selected Measures** — loops the selected measures
- **MIDI → Play Selected Measures Once** — plays the selection once
- **MIDI → Mute MIDI** — toggles note audio on/off while editing

To select measures, click and drag across them in the score editor.

---

## Exporting to MIDI

**File → Export MIDI** saves the score as a `.mid` file that you can use
with any MIDI player or DAW.

---

## Troubleshooting

### No sound
- Make sure a MIDI synthesiser is running (Qsynth or TiMidity)
- Check **MIDI → Refresh Device List** to re-scan for MIDI devices
- Make sure `python3-pyqt5.qtmultimedia` is installed

### "Playback error — There are inconsistent repeat markings"
Check your repeat barlines. Every repeat start must have a matching
repeat end.

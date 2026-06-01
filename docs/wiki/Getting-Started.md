# Getting Started

## Installation

### Debian / Ubuntu / MX Linux

```bash
sudo apt install python3-pyqt5 python3-pygame pyqt5-dev-tools lilypond
```

`python3-pygame` is used for MIDI playback. JACK, TiMidity, Qsynth, and other
extra MIDI synthesizer stacks are not required for a normal DrumBurp test run.

### Running the program

```bash
./run-drumburp.sh
```

Or manually:

```bash
export PYTHONPATH="$PWD/src"
python3 src/DrumBurp.py
```

---

## Creating your first score

1. Open DrumBurp
2. Go to **File → New** (Ctrl+N)
3. Choose the number of measures, the beat count, and the drum kit
4. Click **OK**

A new blank score appears in the editor.

---

## Adding notes

- **Left click** on a drum line at the position you want → toggles the default
  note head on/off
- **Middle click** → cycles through the available note heads for that drum
- **Right click** → opens a context menu with more options

---

## Editing score properties

Go to **Score → Edit Score Properties** to set:

- **Title** — the name of the song
- **Artist** — the artist or band name
- **Tabbed by** — your name as the transcriber
- **BPM** — tempo in beats per minute
- **Swing** — swing feel (No / 8ths / 16ths / 32nds)

> **Note:** When you create a new score, the default values are
> "Untitled", "Unknown", and "Nobody". These are stored inside the `.brp`
> file. If you open an existing file that was created before the
> internationalization update, those default strings will still appear in
> English even when running in Spanish. To change them, edit the score
> properties manually via **Score → Edit Score Properties**
> (or **Partitura → Propiedades de la partitura** in Spanish).

---

## Saving and opening files

- **File → Save** (Ctrl+S) — saves to the current `.brp` file
- **File → Save As** — saves to a new file
- **File → Open** (Ctrl+O) — opens a `.brp` file
- Recent files are listed under **File → Recent Scores**

---

## Navigating the score

- Use the **Section navigator** dropdown (top toolbar) to jump to any
  named section
- Use the scroll bars or mouse wheel to scroll
- **View → Fit Window** — adjusts the score width to fill the window
- **View → Fit Page** — adjusts the score width to fit the selected paper size

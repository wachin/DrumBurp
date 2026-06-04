# DrumBurp Wiki

Welcome to the DrumBurp manual. DrumBurp is a simple GUI for creating and
editing drum music notation.

**This fork** is a port of the original
[DrumBurp by Michael Thomas](https://github.com/Whatang/DrumBurp)
to Python 3 and PyQt5, maintained by Washington Indacochea Delgado.

---

## Pages

- [[Getting Started]]
- [[Score Properties and Metadata]]
- [[Measure Counts]]
- [[Drum Kit Editor]]
- [[Lilypond Export]]
- [[MIDI Playback]]
- [[ASCII Export]]
- [[Internationalization (i18n)]]
- [[Keyboard Shortcuts]]
- [[Building from Source]]

---

## Quick start

1. Install dependencies:
   ```bash
   sudo apt install python3-pyqt5 python3-pygame pyqt5-dev-tools lilypond
   ```
2. Run:
   ```bash
   ./run-drumburp.sh
   ```
3. Create a new score: **File → New** (Ctrl+N)
4. Click on a line in the score to add a note
5. Right-click for options on any element

---

## Reporting issues

Please open an issue at:
https://github.com/wachin/DrumBurp/issues

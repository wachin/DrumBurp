# ASCII Export

DrumBurp can export your score as a plain text file — a format widely used
for sharing drum tabs online in forums, emails, and text documents.

---

## Using the Export Text tab

Click the **Exportar texto** (Export Text) tab in the main window to see
a live preview of the ASCII output with the current settings.

The preview updates automatically as you change options or edit the score.

---

## Export options

| Option | Default | Description |
|--------|---------|-------------|
| **Song info** | On | Includes title, artist, tabber name, BPM and date at the top |
| **Drum kit key** | On | Lists each drum abbreviation and its full name |
| **Omit empty lines for unlocked drums** | On | Hides drum lines that have no notes (locked lines are always shown) |
| **Beat count** | On | Prints the beat count (e.g. `1 + 2 + 3 + 4 +`) below each staff |
| **Underline section titles with ~ characters** | On | Adds a `~~~` underline under each section title |
| **Surround section titles with brackets** | Off | Wraps section titles in `[square brackets]` |
| **Empty line before section title** | Off | Adds a blank line before each section title |
| **Empty line after section title** | Off | Adds a blank line after each section title |

---

## Saving to a file

Click **File → Export ASCII** (or the **Export to file** button in the
Export Text tab) to save the output to a `.txt` file.

---

## Example output

```
Title     : My Song
Artist    : The Band
BPM       : 120
Tabbed by : Washington
Date      : 14 May 2026

Cr - Crash
Hh - Hi-Hat
Sn - Snare
Bd - Kick

== Verse ==
~~~~~~~~~

Cr |x---------------|x---------------|
Hh |-x-x-x-x-x-x-x-|-x-x-x-x-x-x-x-|
Sn |----o-------o---|----o-------o---|
Bd |o-------o-------|o-------o-------|
   |1 + 2 + 3 + 4 + |1 + 2 + 3 + 4 + |
```

---

## Note symbols

The symbols used in the ASCII output come from the note heads defined in
the drum kit. The default kit uses:

| Symbol | Meaning |
|--------|---------|
| `x` | Normal hit (e.g. hi-hat closed, ride) |
| `o` | Open hit (e.g. hi-hat open, bass drum) |
| `O` | Accent |
| `g` | Ghost note |
| `f` | Flam |
| `d` | Drag |
| `+` | Choke / foot hi-hat |
| `-` | Empty (no note) |
| `\|` | Barline |
| `/` | Repeat start |
| `\` | Repeat end |

---

## Repeat markings

Repeats are shown using `/` (repeat start) and `\` (repeat end) at the
barline positions. Alternate endings are shown with their number above
the staff.

---

## Swing notation

If the score has a swing setting, a line is added to the header:

```
Swung 8ths
```

---

## Tips

- Use **Fit Page** (View → Fit Page) before exporting to make sure the
  staff width matches your target page or screen width.
- The **Omit empty lines** option keeps the output compact — useful for
  scores where only a few drums are active at a time.
- Section titles help readers navigate long scores. Add them by
  right-clicking on a barline and selecting **Set section end**.

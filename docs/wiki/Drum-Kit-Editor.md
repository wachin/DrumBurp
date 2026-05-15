# Drum Kit Editor

The Drum Kit Editor lets you define which drums are in your kit, how they
look in the score, how they sound through MIDI, and how they appear in
Lilypond notation.

Open it with **Score → Edit Drum Kit**.

> **Warning:** Editing the kit cannot be undone. DrumBurp will ask you to
> confirm before applying changes.

---

## Overview of the interface

The editor is divided into three panels:

| Panel | What it controls |
|-------|-----------------|
| Left — Drums | The list of drums in the kit and their order |
| Centre — Drum Info / Note Heads | Name, abbreviation, and note head symbols for the selected drum |
| Right — Lilypond Notation / MIDI | How the selected note head looks in Lilypond and sounds in MIDI |

---

## Managing drums

### Adding a drum

Click **Add** (the `+` button in the Drums panel). A new drum called
"New drum" is added at the bottom of the list. Type a name and a
two-character abbreviation.

### Removing a drum

Select a drum and click **Delete**. You cannot delete the last remaining drum.

### Reordering drums

Select a drum and click the **Up** or **Down** arrows. The order in the
list determines the order of lines in the score (bottom of the list =
top line in the score).

### Locking a drum line

Check **Line Lock** to keep a drum line always visible in the score, even
if it has no notes. Locked lines are also protected from the
**Delete empty non-locked drums** operation.

---

## Drum name and abbreviation

- **Name** — the full name shown in the drum key at the top of the score
  (e.g. `Hi-Hat`)
- **Abbreviation** — the 1–2 character label shown on each line in the
  score (e.g. `Hh`)

The abbreviation must be unique within the kit.

### Convert from existing drum

The **Convert from existing drum** dropdown lets you map notes from an
existing drum in the current score to the new drum. This is useful when
renaming or reorganising drums without losing your notes.

---

## Note heads

Each drum can have multiple note head symbols. For example, a hi-hat might
have `x` (closed), `o` (open), and `+` (foot).

### Adding a note head

Click **Add** in the Note Heads section. A new note head is added using
the next available symbol.

### Setting the default note head

The default note head is the one placed when you left-click on the drum
line in the score. Select a note head and click **Set Default** to make
it the default.

### Keyboard shortcuts

Each note head has a keyboard shortcut — a single letter you can press
while hovering over the drum line to toggle that note head. Shortcuts are
assigned automatically but can be changed with the **Shortcut** dropdown.

The current shortcuts are shown in the **Head (Shortcut)** display at the
bottom right of the main window when you hover over a drum line.

---

## Lilypond notation settings

These settings control how the note head appears when you export to
Lilypond.

| Setting | Description |
|---------|-------------|
| **Head** | The notehead shape: default, cross, diamond, harmonic, triangle, xcircle |
| **Effect** | Articulation: none, open, stopped, ghost, flam, choke, accent, drag |
| **Stem up** | Whether the note stem prefers to go up or down |
| **Move up / Move down** | Adjusts the vertical position of the note on the staff |

The **Notation display** preview shows how the note will look in Lilypond
output.

---

## MIDI settings

| Setting | Description |
|---------|-------------|
| **MIDI Note** | The General MIDI percussion note number (e.g. 38 = Snare) |
| **Volume** | The velocity (loudness) of this note head (0–127) |
| **Effects** | MIDI playback effect: Normal, Accent, Ghost, Choke, Flam, Drag |

Click **Sound** to toggle MIDI audio on/off while editing the kit.

---

## Kit files

### Saving a kit

Click **Save** to save the current kit to a `.dbk` file. You can reload
it later in any score.

### Loading a kit

Click **Load** to load a kit from a `.dbk` file.

### Default kits

Click **Default kits** to open the Default Kit Manager, where you can:

- Load one of DrumBurp's built-in kits (Standard, Jazz, etc.)
- Save the current kit as a named default for future use
- Overwrite or delete your saved defaults

### Resetting the kit

- **Reset** — reverts the kit to the state it was in when you opened the
  editor (discards all changes made in this session)
- **New kit** — clears all drums and starts from scratch

### Delete empty non-locked drums

Removes all drums that have no notes in the current score and are not
locked. Useful for cleaning up a kit after importing or converting.

---

## Applying changes

Click **OK** to apply the kit changes to the score. This operation cannot
be undone — DrumBurp will ask for confirmation first.

Click **Cancel** to discard all changes and keep the original kit.

# Score Properties and Metadata

## Editing score properties

Go to **Score → Edit Score Properties** to open the properties dialog.

| Field | Description |
|-------|-------------|
| Title | The name of the song |
| Artist | The artist or band |
| Tabbed by | The person who wrote this transcription |
| BPM | Tempo in beats per minute |
| Swing | Swing feel: No / 8ths / 16ths / 32nds |

These fields appear at the top of the score in the editor and are included
in Lilypond and ASCII exports.

---

## Default values for new scores

When you create a new score (**File → New**), the default values are:

| Field | Default (English) | Default (Spanish) |
|-------|-------------------|-------------------|
| Title | Untitled | Sin titulo |
| Artist | Unknown | Desconocido |
| Tabbed by | Nobody | Nadie |

> **Important:** These defaults are stored as literal text inside the `.brp`
> file at the moment the score is created. If you open a `.brp` file that
> was created before the internationalization update, the fields will still
> contain the original English strings ("Untitled", "Unknown", "Nobody")
> even when running DrumBurp in Spanish.
>
> To update them, open the file and go to
> **Score → Edit Score Properties** (Spanish: **Partitura → Propiedades de
> la partitura**) and change the fields manually.

---

## Showing and hiding metadata

Use the **View** menu to toggle visibility:

- **Show Score Info** — shows/hides the title, artist, tabber and BPM at
  the top of the score
- **Show BPM** — shows/hides the BPM value specifically

---

## Score width and page size

- **Score Properties panel** (right side of toolbar) — set the number of
  columns and the paper size
- **View → Fit Window** — auto-sets width to fill the current window
- **View → Fit Page** — auto-sets width to fit the selected paper size

The paper size affects how many pages the score uses and how it looks when
printed or exported to PDF.

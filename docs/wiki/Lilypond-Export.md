# Lilypond Export

DrumBurp can export your score to
[LilyPond](https://lilypond.org/) format and use LilyPond to generate
high-quality sheet music as PDF, PostScript, or PNG.

---

## Requirements

Install LilyPond:

```bash
sudo apt install lilypond
```

The version tested with this fork is **LilyPond 2.24.x**.

---

## Using the Lilypond Output tab

1. Click the **Salida de Lilypond** (Lilypond Output) tab
2. Set your options in the toolbar:
   - **Pages** — force a specific number of pages (0 = let LilyPond decide)
   - **Size** — global staff size (default 20)
   - **Fill last page** — fill the last page with music
   - **PDF / PS / PNG** — output format
3. Click **Set Path** (Ruta) the first time to point DrumBurp to the
   `lilypond` executable (usually `/usr/bin/lilypond`)
4. Click **Vista previa** (Preview) to generate and display the output
5. After the first preview, the button changes to **Actualizar** (Refresh)

---

## Exporting to a file

Use **File → Export Lilypond** to save the `.ly` source file and run
LilyPond on it. The output file (PDF/PS/PNG) is saved next to the `.ly` file.

---

## Troubleshooting

### "Lilypond impossible"
The score contains something that cannot be expressed in LilyPond notation.
Check for unusual time signatures or note combinations.

### "Build failed!"
LilyPond ran but returned an error. This usually means the generated `.ly`
file has a syntax issue. Check the LilyPond version:

```bash
lilypond --version
```

This fork requires LilyPond **2.22 or later**. Older versions used
`"open"` and `"stopped"` as quoted strings for percussion articulations;
LilyPond 2.22+ requires them as unquoted Scheme symbols. This fork
handles that automatically.

### LilyPond not found
Click **Ruta** (Path) in the Lilypond Output tab and navigate to the
`lilypond` executable. On Debian/Ubuntu it is usually `/usr/bin/lilypond`.

---

## Score metadata in Lilypond output

The title, artist, and tabber fields from the score properties appear in
the LilyPond header:

```lilypond
\header {
  title = "My Song"
  composer = "The Artist"
  arranger = "Tabbed by Nobody"
}
```

To change these, edit **Score → Edit Score Properties** before exporting.

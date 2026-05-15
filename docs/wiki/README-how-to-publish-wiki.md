# GitHub Wiki — status and maintenance

The wiki is live at: **https://github.com/wachin/DrumBurp/wiki**

The files in this `docs/wiki/` folder are the source for the wiki pages.
Edit them here, then copy the updated content to the wiki.

---

## Wiki pages

| File in docs/wiki/ | Wiki URL |
|--------------------|----------|
| `Home.md` | https://github.com/wachin/DrumBurp/wiki |
| `Getting-Started.md` | https://github.com/wachin/DrumBurp/wiki/Getting-Started |
| `Score-Properties-and-Metadata.md` | https://github.com/wachin/DrumBurp/wiki/Score-Properties-and-Metadata |
| `Drum-Kit-Editor.md` | https://github.com/wachin/DrumBurp/wiki/Drum-Kit-Editor |
| `Lilypond-Export.md` | https://github.com/wachin/DrumBurp/wiki/Lilypond-Export |
| `MIDI-Playback.md` | https://github.com/wachin/DrumBurp/wiki/MIDI-Playback |
| `ASCII-Export.md` | https://github.com/wachin/DrumBurp/wiki/ASCII-Export |
| `Keyboard-Shortcuts.md` | https://github.com/wachin/DrumBurp/wiki/Keyboard-Shortcuts |
| `Internationalization.md` | https://github.com/wachin/DrumBurp/wiki/Internationalization |
| `Building-from-Source.md` | https://github.com/wachin/DrumBurp/wiki/Building-from-Source |

---

## Updating a wiki page

**Option A — Edit directly on GitHub:**
1. Go to the wiki page URL above
2. Click the **Edit** pencil icon
3. Make your changes and save

**Option B — Clone the wiki repo (faster for multiple pages):**

```bash
git clone https://github.com/wachin/DrumBurp.wiki.git
cd DrumBurp.wiki

# Copy updated files from docs/wiki/
cp ../DrumBurp/docs/wiki/Getting-Started.md .

git add .
git commit -m "Update Getting Started page"
git push
```

---

## Adding a new wiki page

1. Add a new `.md` file to `docs/wiki/` in this repository
2. Either create it on the GitHub wiki UI, or clone the wiki repo and push

---

## Pages still to write

All pages are now written. The wiki is complete.

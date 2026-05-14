# How to publish these files as a GitHub Wiki

The files in this folder are the content for the DrumBurp GitHub Wiki.
Each `.md` file becomes one wiki page.

## Step 1 — Enable the Wiki on GitHub

1. Go to https://github.com/wachin/DrumBurp
2. Click **Settings** (top right tab)
3. Scroll down to **Features**
4. Check **Wikis**
5. Click **Save**

## Step 2 — Create the first page

1. Go to https://github.com/wachin/DrumBurp/wiki
2. Click **Create the first page**
3. The page name must be **Home** (this is the wiki front page)
4. Copy the content of `docs/wiki/Home.md` into the editor
5. Click **Save Page**

## Step 3 — Add the remaining pages

For each file below, click **New Page** on the wiki, use the filename
(without `.md`) as the page title, and paste the content:

| File | Wiki page title |
|------|----------------|
| `Getting-Started.md` | Getting Started |
| `Score-Properties-and-Metadata.md` | Score Properties and Metadata |
| `Lilypond-Export.md` | Lilypond Export |
| `MIDI-Playback.md` | MIDI Playback |
| `Keyboard-Shortcuts.md` | Keyboard Shortcuts |
| `Internationalization.md` | Internationalization (i18n) |
| `Building-from-Source.md` | Building from Source |

## Step 4 — Clone the wiki for easier editing (optional)

GitHub Wikis are Git repositories. You can clone and push directly:

```bash
git clone https://github.com/wachin/DrumBurp.wiki.git
cd DrumBurp.wiki
# Copy files from docs/wiki/ here, then:
git add .
git commit -m "Add wiki pages"
git push
```

This is the fastest way to publish all pages at once.
